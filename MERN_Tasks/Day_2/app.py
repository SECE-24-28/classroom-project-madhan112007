from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["LoginDB"]
users = db["users"]

# Home → Redirect to Login
@app.route("/")
def home():
    return render_template("login.html")

# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        users.insert_one({
            "username": username,
            "email": email,
            "password": password
        })

        return "<h3>Signup Successful! <a href='/login'>Go to Login</a></h3>"

    return render_template("signup.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({"email": email, "password": password})

        if user:
            return f"""
                <h2>Welcome {user['username']}!</h2>
                <a href='/login'>Back to Login</a>
            """
        else:
            return "<h3>Invalid credentials! <a href='/login'>Try Again</a></h3>"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
