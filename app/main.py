from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://areefhussain099:********areef@cluster099.ny6vqpr.mongodb.net/")
db = client["flask_db"]
collection = db["users"]

# Route to show the form
@app.route('/')
def index():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    # Insert into MongoDB
    collection.insert_one({"name": name, "email": email})
    return f"✅ Data submitted successfully! Name: {name}, Email: {email}"

if __name__ == '__main__':
    app.run(debug=True)
