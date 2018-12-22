from flask import Flask, render_template, request, json, url_for, redirect
from backend import *

dbms = DBMS("166.111.71.220", "1521", "dbta")
dbms.login(user="s2016011246", password="19980211")

app = Flask(__name__, static_url_path='/templates')

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/data_cook/<cook_id>', methods=['POST', 'GET'])
def data_cook(cook_id):
    if request.method=="POST":
        dish_id = request.form['dishid']
        order_id = request.form['orderid']
        dbms.action_cook(dish_id, order_id)
    identity, dishes = dbms.query_cook(cook_id)
    ident = identity[1]
    return render_template("cook.html", identity=ident, dishes=dishes, thisid=cook_id)

@app.route('/data_waiter/<waiter_id>', methods=['POST', 'GET'])
def data_waiter(waiter_id):
    if request.method=="POST":
        if(request.form["customerid"]!="" and request.form["customername"]!=""):
            if(request.form["birthday"]!=""):
                dbms.insert_customer(customerNo=request.form["customerid"], customerName=request.form["customername"],
                             birthday=request.form["birthday"], phone=request.form["phone"], email=request.form["email"])
            else:
                dbms.insert_customer(customerNo=request.form["customerid"], customerName=request.form["customername"],
                                     phone=request.form["phone"], email=request.form["email"])
        dish_id = request.form['dishid']
        order_id = request.form['orderid']
        dbms.action_waiter(dish_id, order_id)
    identity, dishes = dbms.query_waiter(waiter_id)
    ident = identity[1]
    return render_template("waiter.html", identity=ident, dishes=dishes, thisid=waiter_id)


@app.route('/data_waiter2/<waiter_id>', methods=['POST', 'GET'])
def data_waiter2(waiter_id):
    if request.method=="POST":
        dish_id = request.form['dishid']
        order_id = request.form['orderid']
        dbms.action_waiter(dish_id, order_id)
    identity, dishes = dbms.query_waiter(waiter_id)
    ident = identity[1]
    return render_template("waiter.html", identity=ident, dishes=dishes, thisid=waiter_id)

@app.route('/cook', methods=['POST', 'GET'])
def login_cook():
    if request.method=="POST":
        id = request.form['id']
        pw = request.form['pw']
        if(len(id)<=10 and len(pw)<=20):
            if(dbms.validate(id, pw, "c")):
                print("Login with cook: ", id)
                identity, dishes = dbms.query_cook(id)
                return render_template('cook.html', thisid=id, identity=identity[1], dishes=dishes)
        return render_template('login_cook.html', error=True)
    return render_template("login_cook.html")

@app.route('/customer', methods=['POST', 'GET'])
def login_customer():
    if request.method=="POST":
        id = request.form['id']
        pw = request.form['pw']
        if(len(id)<=20 and len(pw)<=20):
            if(dbms.validate(id, pw, "x")):
                print("Login with customer: ", id)
                return render_template('customer.html', thisid=id)
        return render_template('login_customer.html', error=True)
    return render_template("login_customer.html", error=False)


@app.route('/waiter', methods=['POST', 'GET'])
def login_waiter():
    if request.method=="POST":
        id = request.form['id']
        pw = request.form['pw']
        if(len(id)<=10 and len(pw)<=20):
            if(dbms.validate(id, pw, "w")):
                print("Login with waiter: ", id)
                identity, dishes = dbms.query_waiter(id)
                return render_template('waiter.html', thisid=id, dishes=dishes)
        return render_template('login_waiter.html', error=True)
    return render_template("login_waiter.html", error=False)

@app.route('/admin', methods=['POST', 'GET'])
def login_admin():
    if request.method=="POST":
        id = request.form['id']
        pw = request.form['pw']
        if(len(id)<=10 and len(pw)<=20):
            if(dbms.validate(id, pw, "a")):
                print("Login with admin: ", id)
                return render_template('admin.html', thisid=id)
        return render_template('login_admin.html', error=True)
    return render_template("login_admin.html", error=False)

@app.route('/test')
def show_test():
    return render_template('menu.html')


if __name__ == '__main__':
    app.run(debug=True)
