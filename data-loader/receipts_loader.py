import mysql.connector
import json
from datetime import datetime


def parse_value(value,is_date=False):
    if value is None:
        return None
    if is_date:
        return datetime.utcfromtimestamp(value["$date"] / 1000).strftime('%Y-%m-%d')
    if isinstance(value, dict) and "$oid" in value:
        return value["$oid"]
    return value

def get_conn(host,user,password,database):
    conn=mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

def get_date_key(conn,date_value):
    cursor=conn.cursor()
    try:
        if date_value is not None:
            cursor.execute(f"SELECT date_key FROM rewards_db.dim_date WHERE date='{date_value}'")
            result=cursor.fetchone()
            return result[0] if result else 0
        else:
            return 0
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error executing query"
    finally:
        cursor.close()

def get_user_id(conn,user_id):
    cursor=conn.cursor()
    try:
        if user_id is not None:
            cursor.execute(f"SELECT id FROM rewards_db.dim_users WHERE id='{user_id}'")
            result=cursor.fetchone()
            return result[0] if result else "User ID is not found in the user table"
        else:
            return "User ID is None"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error executing query"
    finally:
        cursor.close()

def get_brand_id(conn,barcode):
    cursor=conn.cursor()
    try:
        if barcode is not None and barcode!='511111704140':
            cursor.execute(f"SELECT id FROM rewards_db.dim_brands WHERE barcode='{barcode}'")
            result=cursor.fetchone()
            return result[0] if result else "BrandID not found in brand table"
        else:
            return "Barcode is null"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error executing query"
    finally:
        cursor.close()

def truncate_staging_table(conn,table_name):
    cursor=conn.cursor()
    try:
        cursor.execute(f"TRUNCATE TABLE {table_name}")
        conn.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error executing query"
    finally:
        cursor.close()

def load_staging_table(file_path,conn,table_name):
    cursor=conn.cursor()
    try:
        with open(file_path, "r") as f:
            for line in f:
                data=json.loads(line.strip())
                if table_name == "receipts_staging":
                    insert_query="""INSERT INTO rewards_db.receipts_staging(id,bonus_points_earned,bonus_points_earned_reason,create_date_key, 
                                                            date_scanned_key,finished_date_key,modify_date_key,points_awarded_date_key, 
                                                            points_earned,purchase_date_key,purchased_item_count,rewards_receipt_status,total_spent,user_id)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
                    cursor.execute(insert_query, (
                        parse_value(data["_id"]),
                        parse_value(data.get("bonusPointsEarned")),
                        parse_value(data.get("bonusPointsEarnedReason")),
                        get_date_key(conn,parse_value(data.get("createDate"),is_date=True)),
                        get_date_key(conn,parse_value(data.get("dateScanned"),is_date=True)),
                        get_date_key(conn,parse_value(data.get("finishedDate"),is_date=True)),
                        get_date_key(conn,parse_value(data.get("modifyDate"),is_date=True)),
                        get_date_key(conn,parse_value(data.get("pointsAwardedDate"),is_date=True)),
                        parse_value(data.get("pointsEarned")),
                        get_date_key(conn,parse_value(data.get("purchaseDate"),is_date=True)),
                        parse_value(data.get("purchasedItemCount")),
                        parse_value(data.get("rewardsReceiptStatus")),
                        parse_value(data.get("totalSpent")),
                        get_user_id(conn,parse_value(data.get("userId")))
                    ))

                elif table_name == "rewards_receipt_item_staging":
                    rewards_list=data.get("rewardsReceiptItemList", [])
                    if get_date_key(conn,parse_value(data.get("createDate"),is_date=True))!=0 and get_date_key(conn,parse_value(data.get("dateScanned"),is_date=True))!=0 and get_date_key(conn,parse_value(data.get("finishedDate"),is_date=True)) and get_date_key(conn,parse_value(data.get("modifyDate"),is_date=True)) and get_date_key(conn,parse_value(data.get("pointsAwardedDate"),is_date=True)) and 'User ID' not in get_user_id(conn,parse_value(data.get("userId"))):
                        for item in rewards_list:
                            insert_query="""INSERT INTO rewards_db.rewards_receipt_item_staging (id,receipt_id,brand_id,description,final_price, 
                                                                                item_price,needs_fetch_review,partner_item_id, 
                                                                                prevent_target_gap_points,quantity_purchased, 
                                                                                user_flagged_barcode,user_flagged_new_item, 
                                                                                user_flagged_price,user_flagged_quantity)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """

                            cursor.execute(insert_query, (
                                str(parse_value(data["_id"])) + str(parse_value(item.get("barcode"))),
                                parse_value(data["_id"]),
                                get_brand_id(conn,parse_value(item.get("barcode"))),
                                parse_value(item.get("description")),
                                parse_value(item.get("finalPrice")),
                                parse_value(item.get("itemPrice")),
                                parse_value(item.get("needsFetchReview")),
                                parse_value(item.get("partnerItemId")),
                                parse_value(item.get("preventTargetGapPoints")),
                                parse_value(item.get("quantityPurchased")),
                                parse_value(item.get("userFlaggedBarcode")),
                                parse_value(item.get("userFlaggedNewItem")),
                                parse_value(item.get("userFlaggedPrice")),
                                parse_value(item.get("userFlaggedQuantity"))
                            ))

        conn.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error executing query"
    finally:
        cursor.close()

def upsert_receipts_table(conn):
    cursor=conn.cursor()
    try:
        upsert_query="""INSERT INTO rewards_db.fact_receipts(id,bonus_points_earned,bonus_points_earned_reason,create_date_key, 
                                              date_scanned_key,finished_date_key,modify_date_key,points_awarded_date_key, 
                                              points_earned,purchase_date_key,purchased_item_count,rewards_receipt_status, 
                                              total_spent,user_id)
        SELECT id,bonus_points_earned,bonus_points_earned_reason,create_date_key, 
               date_scanned_key,finished_date_key,modify_date_key,points_awarded_date_key,points_earned, 
               purchase_date_key,purchased_item_count,rewards_receipt_status,total_spent,user_id
        FROM ( SELECT * FROM rewards_db.receipts_staging WHERE user_id NOT LIKE 'User ID %' and create_date_key!=0 and date_scanned_key!=0 and finished_date_key!=0 and modify_date_key!=0 and points_awarded_date_key!=0 and purchase_date_key!=0 ) temp
        ON DUPLICATE KEY UPDATE
            bonus_points_earned=VALUES(bonus_points_earned),
            bonus_points_earned_reason=VALUES(bonus_points_earned_reason),
            create_date_key=VALUES(create_date_key),
            date_scanned_key=VALUES(date_scanned_key),
            finished_date_key=VALUES(finished_date_key),
            modify_date_key=VALUES(modify_date_key),
            points_awarded_date_key=VALUES(points_awarded_date_key),
            points_earned=VALUES(points_earned),
            purchase_date_key=VALUES(purchase_date_key),
            purchased_item_count=VALUES(purchased_item_count),
            rewards_receipt_status=VALUES(rewards_receipt_status),
            total_spent=VALUES(total_spent),
            user_id=VALUES(user_id)    
        """
        cursor.execute(upsert_query)
        conn.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error executing query"
    finally:
        cursor.close()

def upsert_rewards_receipt_item_table(conn):
    cursor=conn.cursor()
    try:
        upsert_query="""
        INSERT INTO rewards_db.fact_rewards_receipt_item(id,receipt_id,brand_id,description,final_price, 
                                                         item_price,needs_fetch_review,partner_item_id, 
                                                         prevent_target_gap_points,quantity_purchased, 
                                                         user_flagged_barcode,user_flagged_new_item, 
                                                         user_flagged_price,user_flagged_quantity)
        SELECT id,receipt_id,brand_id,description,final_price, 
               item_price,needs_fetch_review,partner_item_id, 
               prevent_target_gap_points,quantity_purchased, 
               user_flagged_barcode,user_flagged_new_item, 
               user_flagged_price,user_flagged_quantity
        FROM (SELECT * FROM rewards_db.rewards_receipt_item_staging WHERE brand_id NOT LIKE 'BrandID %' AND brand_id NOT LIKE 'Barcode %'
     ) temp
        ON DUPLICATE KEY UPDATE
            receipt_id=VALUES(receipt_id),
            brand_id=VALUES(brand_id),
            description=VALUES(description),
            final_price=VALUES(final_price),
            item_price=VALUES(item_price),
            needs_fetch_review=VALUES(needs_fetch_review),
            partner_item_id=VALUES(partner_item_id),
            prevent_target_gap_points=VALUES(prevent_target_gap_points),
            quantity_purchased=VALUES(quantity_purchased),
            user_flagged_barcode=VALUES(user_flagged_barcode),
            user_flagged_new_item=VALUES(user_flagged_new_item),
            user_flagged_price=VALUES(user_flagged_price),
            user_flagged_quantity=VALUES(user_flagged_quantity);
        """
        cursor.execute(upsert_query)
        conn.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error executing query"
    finally:
        cursor.close()

def process_receipts_file(file_path):
    conn=get_conn("localhost","slq_interview","password","rewards_db")

    truncate_staging_table(conn,"receipts_staging")
    print("Truncated the receipts_staging")

    truncate_staging_table(conn,"rewards_receipt_item_staging")
    print("Truncated the rewards_receipt_item_staging")

    load_staging_table(file_path,conn, "receipts_staging")
    print("Loaded the data in receipts_staging")

    load_staging_table(file_path,conn,"rewards_receipt_item_staging")
    print("Loaded the data in  rewards_receipt_item_staging")

    upsert_receipts_table(conn)
    print("Upsert completed for  fact_receipts")

    upsert_rewards_receipt_item_table(conn)
    print("Upsert completed for  fact_rewards_receipt_item")

    conn.close()

process_receipts_file("/Users/shabeenasultana/PycharmProjects/interview/fetch/Final_Code/fetch-rewards-systems/data-loader/receipts.json")