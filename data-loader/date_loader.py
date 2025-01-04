import mysql.connector
from datetime import datetime, timedelta

#Function to get the mysql connection.
def get_conn(host,user,password,database):
    conn=mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

# Function to populate dim_date
def populate_dim_date(start_date,end_date):
    conn=get_conn("localhost", "slq_interview", "password", "sql_interview")
    cursor=conn.cursor()
    current_date=start_date
    while current_date<=end_date:
        date_key=int(current_date.strftime('%Y%m%d'))
        year=current_date.year
        month=current_date.month
        day=current_date.day
        day_of_week=current_date.strftime('%A')
        week=current_date.isocalendar()[1]
        quarter=(month - 1) // 3 + 1
        is_weekend=1 if current_date.weekday() >= 5 else 0

        insert_query="""INSERT INTO rewards_db.dim_date (date_key,date,year,month,day,day_of_week,week,quarter,is_weekend)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(insert_query, (date_key, current_date, year, month, day, day_of_week, week, quarter, is_weekend))
        current_date += timedelta(days=1)

    conn.commit()
    cursor.close()
    conn.close()

populate_dim_date(datetime(2021, 1, 1),datetime(2023, 12, 31))

print("dim_date table populated successfully.")