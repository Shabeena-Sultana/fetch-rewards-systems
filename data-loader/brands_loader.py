import mysql.connector
import json


def parse_value(value):
    if value is None:
        return None
    if isinstance(value, dict) and "$oid" in value:
        return value["$oid"]
    if isinstance(value, dict) and "$id" in value:
        return value["$id"]["$oid"]
    return value

def get_conn(host,user,password,database):
    conn=mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

def truncate_staging_table(conn):
    cursor=conn.cursor()
    cursor.execute("TRUNCATE TABLE rewards_db.brands_staging")
    conn.commit()
    cursor.close()

def load_staging_table(file_path,conn):
    cursor=conn.cursor()

    with open(file_path,"r") as f:
        for line in f:
            brand=json.loads(line.strip())
            insert_staging_query="""INSERT INTO rewards_db.brands_staging(id,barcode,brand_code,category,category_code,cpg,top_brand,name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(insert_staging_query, (
                parse_value(brand["_id"]),
                parse_value(brand.get("barcode")),
                parse_value(brand.get("brandCode")),
                parse_value(brand.get("category")),
                parse_value(brand.get("categoryCode")),
                parse_value(brand.get("cpg")),
                parse_value(brand.get("topBrand")),
                parse_value(brand.get("name"))
            ))
    conn.commit()
    cursor.close()

def upsert_brands_table(conn):
    cursor=conn.cursor()
    upsert_query="""
    INSERT INTO rewards_db.dim_brands(id,barcode,brand_code,category,category_code,cpg,top_brand,name)
    SELECT id,barcode,brand_code,category,category_code,cpg,top_brand,name
    FROM rewards_db.brands_staging
    ON DUPLICATE KEY UPDATE
        barcode=VALUES(barcode),
        brand_code=VALUES(brand_code),
        category=VALUES(category),
        category_code=VALUES(category_code),
        cpg=VALUES(cpg),
        top_brand=VALUES(top_brand),
        name=VALUES(name);
    """
    cursor.execute(upsert_query)
    conn.commit()
    cursor.close()

def process_brands_file(file_path):
    conn=get_conn("localhost","slq_interview","password","rewards_db")
    truncate_staging_table(conn)
    load_staging_table(file_path, conn)
    upsert_brands_table(conn)
    conn.close()
    print("Data loaded and upserted successfully!")

process_brands_file("/fetch/Final_Code/brands.json")