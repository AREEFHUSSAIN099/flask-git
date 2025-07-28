from flask import Flask, render_template, request
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://areefhussain099:38013801areef@cluster099.ny6vqpr.mongodb.net/")
db = client["flask_db"]
collection = db["users"]

# Route to show form
@app.route('/')
def index():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    collection.insert_one({"name": name, "email": email})
    return f"✅ Data submitted successfully! Name: {name}, Email: {email}"

# Route to return JSON data from data.json
@app.route('/jsondata')
def json_data():
    json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(json_path) as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    app.run(debug=True)
