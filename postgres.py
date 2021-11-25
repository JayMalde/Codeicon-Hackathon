# pip install psycopg2
#https://pynative.com/python-postgresql-tutorial/
import psycopg2

conn = psycopg2.connect(
    host="ec2-18-214-243-100.compute-1.amazonaws.com",
    database="dfi4ih5icfnkkl",
    user="rmzmvojdioauqd",
    password="b763ae371dc69381b1f96438a4a4324c7a16f4a1d93808a27e8386c4a6380e45",
    port=5432    
)
print("Opened database successfully")

cur = conn.cursor()
# cur.execute("create table products(product_id int primary key,product_name varchar(100),category varchar(50),price int,time_required int)")
# print("Table created successfully")
# conn.commit()
cur.execute("INSERT INTO products VALUES (1,'dosa','breakfast',80,10)")
print("Records created successfully")
conn.commit()
conn.close()