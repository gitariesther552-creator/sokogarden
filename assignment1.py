from flask import Flask

app = Flask(__name__)

@app.route("/contact")
def contact():
    return "contact us "

@app.route("/products")
def products():
    return"our products"

app.run(debug=True)