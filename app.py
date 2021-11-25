from flask import Flask,request,render_template
import datetime
import pymysql

app = Flask(__name__)

@app.route('/')
def formLogin():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    login_id = request.form['login_id']
    password = request.form['password']
    type = request.form['type']
    print("login_id "+login_id+" and password = "+password+" and type "+type)
    
    con = pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="canteen",
        port=3306
    )
    print("connected")
    cur = con.cursor()
    print("login_id "+login_id+" and password = "+password+" and type "+type)
    sql = "SELECT COUNT(*) FROM login_data WHERE login_id = %s and password = %s and type = %s"
    val = (login_id,password,type)
    cur.execute(sql,val)
    data = cur.fetchall()
    cur.close()
    con.close()
    for item in data:
        print(item[0])
        if(item[0] == 1):
            if(type == 'admin'):
                return render_template('admin.html')
            else:
                return render_template('user.html')
        else:
            print(type)
            print(login_id)
            print(password)
            print(item[0])
            return render_template('error.html')

@app.route('/add-products',methods = ['POST'])
def addProducts():
    timeReq = float(request.form['timeReq'])
    price = float(request.form['price'])
    productName = request.form['productName']
    category = request.form['category']
    status = 'Available'
    productId = int(request.form['productIdActual'])
    login_id = 1
    date_of_record = datetime.datetime.now()
    con = pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="canteen",
        port=3306
    )
    cur = con.cursor()
    try:
        print('Executing SQL')
        sql = "INSERT INTO products VALUES (%s, %s,%s,%s)"
        val = (productId,productName,category,status)
        cur.execute(sql, val)
        sql = "INSERT INTO price(product_id,price, date_of_record, login_id) VALUES (%s, %s,%s,%s)"
        val = (productId, price, date_of_record, login_id)
        cur.execute(sql, val)
        sql = "INSERT INTO time_required(product_id,time_required, date_of_record, login_id) VALUES (%s, %s,%s,%s)"
        val = (productId, timeReq, date_of_record, login_id)
        cur.execute(sql, val)
    except pymysql.InternalError as error:
        code, message = error.args
        print("Error: " +  str(code) +  str(message))
        cur.close()
        con.close()
        return render_template('error.html')
    con.commit()
    cur.close()
    con.close()
    return render_template('success.html')

@app.route('/form-add-products')
def formAddProducts():
    con = pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="canteen",
        port=3306
    )
    cur = con.cursor()
    cur.execute("SELECT COUNT(productId) FROM products")
    data = cur.fetchone()
    productId = data[0]+1
    return render_template('add_products.html',productId = productId)

if __name__ == '__main__':
    app.run(debug=True)