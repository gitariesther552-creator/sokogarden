#import flask module
from flask import *
import pymysql
#pmysql is a python module that enables you to create a connection to the mysql database

import os


#create an app
app = Flask(__name__)
#below we configure where the product image shall be saved.
app.config['UPLOAD_FOLDER'] = 'static/images'


#define the sign up/register the URL
@app.route("/api/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        #get the details passed from the postman
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]
        
        #create a connection to mySQL database by the pymysql module
        connection = pymysql.connect(host="localhost", password="", user="root", database="sokogarden")
        
        #create a cursor
        cursor = connection.cursor()
        
        
        # Check if email already exists
        check_sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(check_sql, (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({
                "message": "user already registered"
            })
        
        #structure the sql query for insert
        #%s,stands for the pre-prepared statements. Its placeholder that will uphold actual values
        sql = "insert into users(username,password, email, phone) values(%s, %s, %s, %s)"
        
        #create a tupple that will hold all data available in variables
        data = (username, password, email, phone)
        
        #by use of a cursor, execute the sql query as you replace the placeholder with the actual values
        cursor.execute(sql, data)
        
        #commit/complete the changes to the database
        connection.commit()
        
        #give a response to the user
        return jsonify({"message" : "user registered successfully"})
    
import pymysql
#below is the sign in api endpoint
@app.route("/api/signin", methods = ["POST"])
def signin():
    if request.method == "POST":
        #extract data from postman
        email = request.form["email"]
        password = request.form["password"]
        
        
        #create a connection between the db
        connection = pymysql.connect(host="localhost", password="", user="root", database="sokogarden")
        
        #create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        #structure the sql query to check wheter the person trying to login already has an account
        sql = "select * from users where email = %s and password = %s"
        
        #create a tuple to hold your details
        data = (email, password)
        
        #by use of the cursor execute the query
        cursor.execute(sql, data)
        
        #check how many rows are returned when the query gets executed
        count = cursor.rowcount
        
        if count == 0:
            return jsonify({"message" : "login failed. please check on details entered"}) 
        else:
            #if the user is there, take the details of the user and store them in a variable and return a success message to the user
            
            user = cursor.fetchone()  
            
            return jsonify({"message" :"login was successful","user":user })
        
# create a route below that is able to add the product al the to the database.


@app.route("/api/addproduct", methods =["POST"])
def home9():
    if request.method == "POST":
        #extract data from postman
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        product_photo = request.files["product_photo"]
        product_category = request.form["product_category"]
        
        #since the product is a type of a file,we shall extract the name of a productand that name shall be stored in the database while the photo of the product shall be store into statistics/images folder
        filename = product_photo.filename
        
        #specify where the image shall be saved
        product_photo.path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        #save the image
        product_photo.save(product_photo.path)
        
        #a connection between the pymysql module and mysql database
        
        connection = pymysql.connect(host="localhost", password="", user="root", database="sokogarden")
        
        #a cursor
        cursor = connection.cursor()
        
        #structure the sql query for insert
        sql = "insert into products_details(product_name,product_description,product_cost,product_photo,product_category) values(%s, %s, %s, %s,%s)"
        
        #create a tuple to hold your details
        data = (product_name, product_description, product_cost,filename,product_category)
        
        #by use of the cursor execute the query
        cursor.execute(sql, data)   
        
         #commit/complete the changes to the database
        connection.commit() 
        
        #give a response to the user
        return jsonify({"message" : "product added successfully"})
    
    
#below is the get product route
@app.route("/api/getproduct", methods=["GET"])
def get_products_details():
    if request.method == "GET":
        #create a connection to the database
        connection = pymysql.connect(host="localhost",user="root", password="", database="sokogarden")
        
        #below is a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        #structure the sql for fetching all products
        sql = "select *FROM products_details"
        
        #by use of avursor execute the sql
        cursor.execute(sql)
        
        #creat a variable that will hold all those products
        products = cursor.fetchall()
        
        #close the connection
        connection.close()
        
        #return the product as the responce
        return jsonify(products)        
        

# Mpesa Payment Route 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        # Extract POST Values sent
        amount = request.form['amount']
        phone = request.form['phone']

        # Provide consumer_key and consumer_secret provided by safaricom
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        # Authenticate Yourself using above credentials to Safaricom Services, and Bearer Token this is used by safaricom for security identification purposes - Your are given Access
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        # Provide your consumer_key and consumer_secret 
        response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        # Get response as Dictionary
        data = response.json()
        # Retrieve the Provide Token
        # Token allows you to proceed with the transaction
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')  # Current Time
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'  # Passkey(Safaricom Provided)
        business_short_code = "174379"  # Test Paybile (Safaricom Provided)
        # Combine above 3 Strings to get data variable
        data = business_short_code + passkey + timestamp
        # Encode to Base64
        encoded = base64.b64encode(data.encode())
        password = encoded.decode()

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password":password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://coding.co.ke/api/confirm.php",
            "AccountReference": "SokoGarden Online",
            "TransactionDesc": "Payments for Products"
        }

        # POPULAING THE HTTP HEADER, PROVIDE THE TOKEN ISSUED EARLIER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        # Specify STK Push  Trigger URL
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  
        # Create a POST Request to above url, providing headers, payload 
        # Below triggers an STK Push to the phone number indicated in the payload and the amount.
        response = requests.post(url, json=payload, headers=headers)
        print(response.text) # 
        # Give a Response
        return jsonify({"message": "An MPESA Prompt has been sent to Your Phone, Please Check & Complete Payment"})


#run the application
app.run(debug=True)