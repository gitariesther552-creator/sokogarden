#import flask module
from flask import *
import pymysql
#pmysql is a python module that enables you to create a connection to the mysql database

#create an app
app = Flask(__name__)



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
        cursor = connection.cursor(pymysql.cursors.DistCursors)
        
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
    



#run the application
app.run(debug=True)