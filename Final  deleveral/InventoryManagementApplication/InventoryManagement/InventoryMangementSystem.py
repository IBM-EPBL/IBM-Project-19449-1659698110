from crypt import methods
import re
from wsgiref import validate
from flask import Flask, render_template,redirect,request, session,flash
import ibm_db

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

#Database Connection 
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME = b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT = 31249;SECURITY = SSL;SSLSererCertificate = DigiCertGlobalRootCA.crt;UID = rnj93429;PWD = kzoIIKcwZ05e4tyW","","")

# Dashboard Details class
class dashboardDetails:
    def __init__(mainDetails,totalStock,currentInventoryStock,lowStocks,nonMovableStocks,totalQuantityStock):
        mainDetails.totalStock = totalStock["1"]
        mainDetails.currentInventoryStock = currentInventoryStock["1"]
        mainDetails.lowStocks = lowStocks["1"]
        mainDetails.nonMovableStocks = nonMovableStocks["1"]
        mainDetails.totalQuantitystock = totalQuantityStock["1"]
        
class stockDetails:
    def __init__(stockDetails,stockId,stockName,stockQty,costPrice,sellingPrice,status):
        stockDetails.stockId = stockId
        stockDetails.stockName = stockName
        stockDetails.stockQty = stockQty
        stockDetails.costPrice = costPrice
        stockDetails.sellingPrice = sellingPrice
        stockDetails.status = status 


@app.route("/")
def home():
    return render_template("inventoryHome.html")

@app.route("/register")
def register():
    return render_template("inventoryRegisterUser.html")

@app.route("/registerUsr",methods=['GET','POST'])
def registerUsr():
    msg = ''
    if request.method == 'POST':
        storeName = request.form['storeName']
        emailId = request.form['emailId']
        password = request.form['password']
        country = request.form['country']
        state = request.form['state']
        validationQuery = "SELECT * FROM SHOPDETAILS WHERE EMAILID = ?"
        validateStmt = ibm_db.prepare(conn,validationQuery)
        ibm_db.bind_param(validateStmt,1,emailId)
        ibm_db.execute(validateStmt)
        account = ibm_db.fetch_assoc(validateStmt)
        if account:
            msg = "Account is Already exists !"
        else:
            query = "INSERT INTO  SHOPDETAILS (STORENAME,EMAILID,USRPASSWORD,COUNTRY,STATE) VALUES(?,?,?,?,?)"
            stmt = ibm_db.prepare(conn,query)
            ibm_db.bind_param(stmt,1,storeName)
            ibm_db.bind_param(stmt,2,emailId)
            ibm_db.bind_param(stmt,3,password)
            ibm_db.bind_param(stmt,4,country)
            ibm_db.bind_param(stmt,5,state)
            ibm_db.execute(stmt)
            msg = "Registration Successfull"
            return render_template("inventoryLogin.html",msg = msg)
    elif request.method == "POST":
            msg = "Please Fill the form"
 
    return render_template("inventoryRegisterUser.html",msg = msg)


@app.route("/login")
def login():
    return render_template("inventoryLogin.html")

@app.route("/loginUsr",methods=["GET","POST"])
def loginUsr():
    msg = ''
    if request.method == 'POST':
        emailId = request.form['emailId']
        password = request.form['password']
        query = "SELECT * FROM SHOPDETAILS WHERE emailId = ? AND usrpassword = ?"
        stmt = ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,emailId)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            session['loggedin'] = True
            session['id']=account["EMAILID"]
            userid = account['EMAILID']
            session['emailId'] = account['EMAILID']
            msg = "Loggin Sucessfull"
            return redirect("/dashboard")
        else:
            msg = "Invalid Email Id or Password !"
            return render_template("inventoryLogin.html",msg = msg)

@app.route("/dashboard")
def dashboard():
    totStockQuery = "SELECT COUNT(*) FROM STOCKDETAILS"
    activeStocksQuery = "SELECT COUNT(*) FROM STOCKDETAILS WHERE STOCKSTATUS = 'Active'"
    lowStocksQuery = "SELECT COUNT(*) FROM STOCKDETAILS WHERE QTYOFSTOCK < 50"
    nonMovableStockQuery = "SELECT COUNT(*) FROM WAREHOUSEDETAILS"
    totalQuantityQuery = "SELECT SUM(QTYOFSTOCK) FROM STOCKDETAILS"
    
    totStock = ibm_db.prepare(conn,totStockQuery)
    activeStocks = ibm_db.prepare(conn,activeStocksQuery)
    lowStocks = ibm_db.prepare(conn,lowStocksQuery)
    nonMovableStocks = ibm_db.prepare(conn,nonMovableStockQuery)
    totalQuantity = ibm_db.prepare(conn,totalQuantityQuery)
    
    ibm_db.execute(totStock)
    ibm_db.execute(activeStocks)
    ibm_db.execute(lowStocks)
    ibm_db.execute(nonMovableStocks)
    ibm_db.execute(totalQuantity)
    
    totalStock = ibm_db.fetch_assoc(totStock)
    activeStock = ibm_db.fetch_assoc(activeStocks)
    lowStock = ibm_db.fetch_assoc(lowStocks)
    nonMovableStock = ibm_db.fetch_assoc(nonMovableStocks)
    totalQuantitystock = ibm_db.fetch_assoc(totalQuantity)
    
    detail = dashboardDetails(totalStock,activeStock,lowStock,nonMovableStock,totalQuantitystock)
    
    saleDetailsQuery = "SELECT * FROM SALES"
    saleDetail = ibm_db.prepare(conn,saleDetailsQuery)
    ibm_db.execute(saleDetail)
    databaseSales = ibm_db.fetch_tuple(saleDetail)
    sales = []
    while databaseSales != False:
        sales.append(databaseSales)
        databaseSales = ibm_db.fetch_tuple(saleDetail)
        
    return render_template("inventoryDashboard.html",details = detail,sales = sales)

@app.route("/stocks")
def stocks():
    stockDetailsQuery = "SELECT * FROM STOCKDETAILS"
    stockDetail = ibm_db.prepare(conn,stockDetailsQuery)
    ibm_db.execute(stockDetail)
    databaseStocks = ibm_db.fetch_tuple(stockDetail)
    stocks = []
    while databaseStocks != False:
        stocks.append(databaseStocks)
        databaseStocks = ibm_db.fetch_tuple(stockDetail)
            
    return render_template("stocks.html",stocks = stocks)

@app.route("/addStocks",methods=["GET","POST"])
def addStocks():
    if request.method == "POST":
        stockName = request.form['stockName']
        qtyStock = request.form['qtyofstock']
        costPrice = request.form['costPrice']
        sellingPrice = request.form['sellingPrice']
        warehouseid = request.form['warehouseId']
        addStocksQuery = "INSERT INTO  STOCKDETAILS (STOCKNAME,QTYOFSTOCK,COSTPRICE,SELLINGPRICE,WAREHOUSE) VALUES(?,?,?,?,?)"
        stmt = ibm_db.prepare(conn,addStocksQuery)
        ibm_db.bind_param(stmt,1,stockName)
        ibm_db.bind_param(stmt,2,qtyStock)
        ibm_db.bind_param(stmt,3,costPrice)
        ibm_db.bind_param(stmt,4,sellingPrice)
        ibm_db.bind_param(stmt,5,warehouseid)
        ibm_db.execute(stmt)
        
        flash("Stocks Added Sucessfully :) ")
        return redirect("/stocks")

@app.route("/editStocks",methods = ["GET","POST"])
def editStocks():
    if request.method == "POST":
        stockId = request.form['stockId']
        stockName = request.form['stockName']
        qtyStock = request.form['qtyofstock']
        costPrice = request.form['costPrice']
        sellingPrice = request.form['sellingPrice']
        warehouseid = request.form['warehouseId']
        addStocksQuery = "UPDATE STOCKDETAILS SET STOCKNAME = ?,QTYOFSTOCK = ?,COSTPRICE = ?,SELLINGPRICE = ?,WAREHOUSE = ? WHERE STOCKID = ?"
        stmt = ibm_db.prepare(conn,addStocksQuery)
        ibm_db.bind_param(stmt,1,stockName)
        ibm_db.bind_param(stmt,2,qtyStock)
        ibm_db.bind_param(stmt,3,costPrice)
        ibm_db.bind_param(stmt,4,sellingPrice)
        ibm_db.bind_param(stmt,5,warehouseid)
        ibm_db.bind_param(stmt,6,stockId)
        ibm_db.execute(stmt)
        return redirect("/stocks")
    
    return render_template("stocks.html")

@app.route("/deleteStocks",methods = ["GET","POST"])
def deleteStocks():
    if request.method == "POST":
        stockId = request.form["stockid"]
        deleteQuery = "DELETE FROM STOCKDETAILS WHERE STOCKID = ?"
        stmt = ibm_db.prepare(conn,deleteQuery)
        ibm_db.bind_param(stmt,1,stockId)
        ibm_db.execute(stmt)
        return redirect("/stocks")
    else:
        return redirect("/stocks")

@app.route("/warehouse")
def inventory():
    warehouseDetailsQuery = "SELECT * FROM WAREHOUSEDETAILS"
    warehouseDetail = ibm_db.prepare(conn,warehouseDetailsQuery)
    ibm_db.execute(warehouseDetail)
    databaseWarehouse = ibm_db.fetch_tuple(warehouseDetail)
    warehouses = []
    while databaseWarehouse != False:
        warehouses.append(databaseWarehouse)
        databaseWarehouse = ibm_db.fetch_tuple(warehouseDetail)
    
    return  render_template("warehouse.html",warehouses = warehouses)


@app.route("/purchases")
def purchases():
    warehouseDetailsQuery = "SELECT * FROM PURCHASES"
    warehouseDetail = ibm_db.prepare(conn,warehouseDetailsQuery)
    ibm_db.execute(warehouseDetail)
    databaseWarehouse = ibm_db.fetch_tuple(warehouseDetail)
    warehouses = []
    while databaseWarehouse != False:
        warehouses.append(databaseWarehouse)
        databaseWarehouse = ibm_db.fetch_tuple(warehouseDetail)
        
    return render_template("purchases.html",warehouses,warehouses)

@app.route("/addPurchases",methods = ["GET","POST"])
def addPurchases():
    if request.method == "POST":
        warehouseId = request.form['warehouseId']
        warehouseName = request.form['warehouseName']
        addWarehouseQuery = "INSERT INTO PURCHASES (WAREHOUSEID,WAREHOUSENAME) VALUES(?,?)"
        stmt = ibm_db.prepare(conn,addWarehouseQuery)
        ibm_db.bind_param(stmt,1,warehouseId)
        ibm_db.bind_param(stmt,2,warehouseName)
        ibm_db.execute(stmt)
        return redirect("/warehouse")

@app.route("/addWarehouse",methods = ["GET","POST"])
def addWarehouse():
    if request.method == "POST":
        warehouseName = request.form['warehouseName']
        warehouseLocation = request.form['warehouseLocation']
        addWarehouseQuery = "INSERT INTO WAREHOUSEDETAILS (WAREHOUSENAME,WAREHOUSELOCATION) VALUES(?,?)"
        stmt = ibm_db.prepare(conn,addWarehouseQuery)
        ibm_db.bind_param(stmt,1,warehouseName)
        ibm_db.bind_param(stmt,2,warehouseLocation)
        ibm_db.execute(stmt)
        return redirect("/warehouse")

@app.route("/viewStocks",methods=["GET","POST"])
def viewStocks():
    if request.method == "POST":
        warehouseId = request.form["warehouseId"]
        stockDetailsQuery = "SELECT * FROM STOCKDETAILS WHERE WAREHOUSE = ?"
        stmt = ibm_db.prepare(conn,stockDetailsQuery)
        ibm_db.bind_param(stmt,1,warehouseId)
        ibm_db.execute(stmt)     
        totalstocks = ibm_db.fetch_tuple(stmt)
        stocks = []
        while totalstocks != False:
            stocks.append(totalstocks)
            totalstocks = ibm_db.fetch_tuple(stmt)
        
        return render_template("warehouseStocks.html",stocks = stocks)  
    

@app.route("/addSales",methods = ["GET","POST"])
def addSales():
    if request.method == "POST":
        customerName = request.form["customerName"]
        price = request.form["price"]
        paymentMode = request.form["paymentMode"]
        addSalesQuery = "INSERT INTO  SALES (CUSTOMERNAME,PRICE,PAYMENTMODE) VALUES(?,?,?)"
        stmt = ibm_db.prepare(conn,addSalesQuery)
        ibm_db.bind_param(stmt,1,customerName)
        ibm_db.bind_param(stmt,2,price)
        ibm_db.bind_param(stmt,3,paymentMode)
        ibm_db.execute(stmt)
        return redirect("/sales")
    
@app.route("/sales")
def orders():
    saleDetailsQuery = "SELECT * FROM SALES"
    saleDetail = ibm_db.prepare(conn,saleDetailsQuery)
    ibm_db.execute(saleDetail)
    databaseSales = ibm_db.fetch_tuple(saleDetail)
    sales = []
    while databaseSales != False:
        sales.append(databaseSales)
        databaseSales = ibm_db.fetch_tuple(saleDetail)
        
    return render_template("sales.html",sales = sales)


@app.route("/payments")
def payments():
    paymentDetailsQuery = "SELECT * FROM PAYMENTS"
    paymentDetail = ibm_db.prepare(conn,paymentDetailsQuery)
    ibm_db.execute(paymentDetail)
    databasePayments = ibm_db.fetch_tuple(paymentDetail)
    payments = []
    while databasePayments != False:
        payments.append(databasePayments)
        databasePayments = ibm_db.fetch_tuple(paymentDetail)
        
    return render_template("payments.html",payments = payments)


@app.route("/addPayment",methods = ["GET","POST"])
def addPayments():
    if request.method == "POST":
        customerName = request.form["customerName"]
        stockName = request.form["stockName"]
        stockQty = request.form["qtyofstock"]
        amount = request.form["amount"]
        warehouseId = request.form["warehouseId"]
        addPaymentsQuery = "INSERT INTO  PAYMENTS (CUSTOMERNAME,AMOUNT,STOCKNAME,STOCKQTY,WAREHOUSEID) VALUES(?,?,?,?,?)"
        stmt = ibm_db.prepare(conn,addPaymentsQuery)
        ibm_db.bind_param(stmt,1,customerName)
        ibm_db.bind_param(stmt,2,amount)
        ibm_db.bind_param(stmt,3,stockName)
        ibm_db.bind_param(stmt,4,stockQty)
        ibm_db.bind_param(stmt,5,warehouseId)
        ibm_db.execute(stmt)
        return redirect("/payments")
    

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('emailId',None)
    msg = "Logout Successfully"
    return render_template("inventoryHome.html",msg = msg)

if __name__ == "__main__":
    app.run(debug = True)