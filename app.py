import pandas as pd
from apriori import apriori
from flask import (Flask, render_template, redirect, request)
from csv import writer
import psycopg2

dataset = pd.read_csv('data.csv',  header = None )
transactions = []
list_of_products=[]
basket=[]
app=Flask(__name__)

totalrows = len(dataset)
totalcol =int( dataset.size /len(dataset) )

for i in range(0, len(dataset)):
    cart = []
    for j in range(0,totalcol):
        if str( dataset.values[i,j] ) != "nan":
            cart.append( str( dataset.values[i,j]  ))            
        if str(dataset.values[i,j]) not in list_of_products:
            list_of_products.append(str(dataset.values[i,j]))  
    transactions.append(cart)


rules = apriori( transactions, min_support = 0.003, min_confidence = 0.04, min_lift = 3)
results = list(rules)

def recommendation(basket):    
    recommendations=[]
    for item in results:
        pair = item[0] 
        items = [x for x in pair]
        for product in basket:
            if items[0]==product:
                # print("Rule: " + items[0] + " -> " + items[1])       
                # print("Support: " + str(item[1]))
                # print("Confidence: " + str(item[2][0][2]))
                # print("Lift: " + str(item[2][0][3]))
                if items[1] not in recommendations:
                    recommendations.append(items[1])
    return recommendations

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        form_items = request.form.getlist('items')
        for item in form_items:
            basket.append(item)
    context = {
        'itemset_count': len(list_of_products),
        'rules_count': len(results),
        'items': list_of_products,
        'basket':basket,
        'recommendations': recommendation(basket),
    }
    return render_template('main.html', **context)

@app.route('/reset-basket/', methods=['POST'])
def reset_basket():
    global basket
    basket = []
    return redirect('/')

@app.route('/menu')
def menu():
    con = psycopg2.connect(
        host="ec2-18-214-243-100.compute-1.amazonaws.com",
        database="dfi4ih5icfnkkl",
        user="rmzmvojdioauqd",
        password="b763ae371dc69381b1f96438a4a4324c7a16f4a1d93808a27e8386c4a6380e45",
        port=5432    
    )
    cur = con.cursor()
    sql = "select product_name,price,time_required,category from products where status='available' order by category"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    con.close()
    return render_template('menu.html',data = data,categoryPrinted = '')

@app.route('/add')
def add():
    return render_template('add_product.html')

@app.route('/add_product',methods = ['POST'])
def addProduct():
    timeReq = float(request.form['timeReq'])
    price = float(request.form['price'])
    productName = request.form['productName']
    productId = request.form['productId']
    category = request.form['category']
    status="available"
    con = psycopg2.connect(
        host="ec2-18-214-243-100.compute-1.amazonaws.com",
        database="dfi4ih5icfnkkl",
        user="rmzmvojdioauqd",
        password="b763ae371dc69381b1f96438a4a4324c7a16f4a1d93808a27e8386c4a6380e45",
        port=5432    
    )
    cur = con.cursor()
    try:
        print('Executing SQL')
        sql = "INSERT INTO products VALUES (%s,%s,%s,%s,%s,%s)"
        val = (productId,productName,category,price,status,timeReq)
        cur.execute(sql, val)
    except psycopg2.InternalError as error:
        code, message = error.args
        print("Error: " +  str(code) +  str(message))
        cur.close()
        con.close()
        return render_template('error.html')
    con.commit()
    cur.close()
    con.close()
    return render_template('success.html')

@app.route('/order')
def order():
    con = psycopg2.connect(
        host="ec2-18-214-243-100.compute-1.amazonaws.com",
        database="dfi4ih5icfnkkl",
        user="rmzmvojdioauqd",
        password="b763ae371dc69381b1f96438a4a4324c7a16f4a1d93808a27e8386c4a6380e45",
        port=5432    
    )
    cur = con.cursor()
    sql = "select product_name,price,time_required,category from products where status='available' order by category"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    con.close()
    return render_template('product_list.html',data = data)

@app.route('/add_order_to_list', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        form_items = request.form.getlist('items')
        with open('data.csv', 'a',newline='\n') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(form_items)
            f_object.close()
        products=','.join(map(str, form_items))
        status="ordered"
        con = psycopg2.connect(
            host="ec2-18-214-243-100.compute-1.amazonaws.com",
            database="dfi4ih5icfnkkl",
            user="rmzmvojdioauqd",
            password="b763ae371dc69381b1f96438a4a4324c7a16f4a1d93808a27e8386c4a6380e45",
            port=5432    
        )
        cur = con.cursor()
        try:
            sql = "INSERT INTO orders(products,status) VALUES (%s,%s)"
            val = (products,status)
            cur.execute(sql, val)
        except psycopg2.InternalError as error:
            code, message = error.args
            print("Error: " +  str(code) +  str(message))
            cur.close()
            con.close()
            return render_template('error.html')
        con.commit()
        cur.close()
        con.close()
    return render_template('success.html')          

@app.route('/update_order_status', methods=['GET', 'POST'])
def order_status():
    
    con = psycopg2.connect(
        host="ec2-18-214-243-100.compute-1.amazonaws.com",
        database="dfi4ih5icfnkkl",
        user="rmzmvojdioauqd",
        password="b763ae371dc69381b1f96438a4a4324c7a16f4a1d93808a27e8386c4a6380e45",
        port=5432    
    )
    cur = con.cursor()
    try:
        sql = "INSERT INTO orders(products,status) VALUES (%s,%s)"
        val = (products,status)
        cur.execute(sql, val)
    except psycopg2.InternalError as error:
        code, message = error.args
        print("Error: " +  str(code) +  str(message))
        cur.close()
        con.close()
        return render_template('error.html')
    con.commit()
    cur.close()
    con.close()
    return render_template('success.html')          

if __name__ == '__main__':
    app.run()