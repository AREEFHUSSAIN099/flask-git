from flask import Flask, render_template, request
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://areefhussain099:301301areef@cluster099.ny6vqpr.mongodb.net/")
db = client["flask_db"]
collection = db["users"]
todo_collection = db["todo_items"]

# Home form (name, email)
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    collection.insert_one({"name": name, "email": email})
    return f"✅ Data submitted successfully! Name: {name}, Email: {email}"

# JSON route
@app.route('/jsondata')
def json_data():
    json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(json_path) as f:
        data = json.load(f)
    return data

# To-Do form page
@app.route('/todo')
def todo():
    return render_template('todo.html')

# To-Do submission route (includes due_date)
@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_id = request.form['itemId']
    item_name = request.form['itemName']
    item_description = request.form['itemDescription']
    due_date = request.form['dueDate']  # New field

    todo_collection.insert_one({
        "item_id": item_id,
        "item_name": item_name,
        "item_description": item_description,
        "due_date": due_date
    })
    return f"✅ To-Do Item submitted! ID: {item_id}, Name: {item_name}, Description: {item_description}, Due Date: {due_date}"

if __name__ == '__main__':
    app.run(debug=True)
