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

# cur.execute("drop table products")
# print("Deleted successfully")

# cur.execute("create table products(product_id int primary key,product_name varchar(100),category varchar(50),price int,status varchar(100),time_required int)")
# print("Table created successfully")
# conn.commit()

# cur.execute("create table orders(order_id serial primary key,products varchar(200),status varchar(100))")
# print("Table created successfully")
# conn.commit()

# cur.execute("INSERT INTO products VALUES (1,'dosa','breakfast',80,'available',10)")
# cur.execute("INSERT INTO products VALUES (2,'idli','breakfast',40,'available',10)")
# cur.execute("INSERT INTO products VALUES (3,'mendu wada','breakfast',50,'available',10)")
# cur.execute("INSERT INTO products VALUES (4,'masala dosa','breakfast',100,'available',10)")
# cur.execute("INSERT INTO products VALUES (5,'poha','breakfast',30,'available',10)")
# print("Records inserted successfully")
# conn.commit()

conn.close()