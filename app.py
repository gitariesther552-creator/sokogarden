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
        



#run the application
app.run(debug=True)