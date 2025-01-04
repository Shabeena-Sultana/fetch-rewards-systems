import mysql.connector
import json
from datetime import datetime

def parse_value(value,is_date=False):
    if value is None:
        return None
    if is_date:
        return datetime.utcfromtimestamp(value["$date"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
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

def truncate_staging_table(conn):
    cursor=conn.cursor()
    cursor.execute("TRUNCATE TABLE rewards_db.users_staging")
    conn.commit()
    cursor.close()

def load_staging_table(file_path,conn):
    cursor=conn.cursor()
    with open(file_path, "r") as f:
        for line in f:
            user=json.loads(line.strip())
            insert_staging_query="""INSERT INTO rewards_db.users_staging(id,state,created_date,last_login,role,active) VALUES (%s,%s,%s,%s,%s,%s)"""
            cursor.execute(insert_staging_query, (
                parse_value(user["_id"]),
                user.get("state"),
                parse_value(user.get("createdDate"), is_date=True),
                parse_value(user.get("lastLogin"), is_date=True),
                user.get("role"),
                user.get("active")
            ))
    conn.commit()
    cursor.close()

def upsert_users_table(conn):
    cursor=conn.cursor()
    upsert_query="""
    INSERT INTO rewards_db.dim_users(id,state,created_date,last_login,role,active)
    SELECT id,state,created_date,last_login,role,active
    FROM users_staging
    ON DUPLICATE KEY UPDATE
        state=VALUES(state),
        created_date=VALUES(created_date),
        last_login=VALUES(last_login),
        role=VALUES(role),
        active=VALUES(active);
    """
    cursor.execute(upsert_query)
    conn.commit()
    cursor.close()

def process_users_file(file_path):
    conn=get_conn("localhost","slq_interview","password","rewards_db")
    truncate_staging_table(conn)
    load_staging_table(file_path, conn)
    upsert_users_table(conn)
    conn.close()
    print("Data loaded and upserted successfully!")

process_users_file("/fetch/Final_Code/users.json")