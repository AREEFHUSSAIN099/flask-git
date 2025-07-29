from flask import Flask, render_template, request
from pymongo import MongoClient
import json
import os
import uuid
import hashlib

app = Flask(__name__)

# ✅ MongoDB connection
client = MongoClient("mongodb+srv://areefhussain099:38013801areef@cluster099.ny6vqpr.mongodb.net/")
db = client["flask_db"]
collection = db["users"]
todo_collection = db["todo_items"]


# ✅ Route for Name & Email form
@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    collection.insert_one({"name": name, "email": email})
    return f"✅ Data submitted successfully! Name: {name}, Email: {email}"


# ✅ JSON route from file
@app.route('/jsondata')
def json_data():
    json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(json_path) as f:
        data = json.load(f)
    return data


# ✅ To-Do Form route
@app.route('/todo')
def todo():
    return render_template('todo.html')


# ✅ To-Do submission with UUID, Hash, optional Category
@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_id = request.form['itemId']
    item_name = request.form['itemName']
    item_description = request.form['itemDescription']
    due_date = request.form['dueDate']
    priority = request.form['priority']

    # ✅ optional field - avoids KeyError
    category = request.form.get('category', 'Not Specified')

    item_uuid = str(uuid.uuid4())
    hash_input = item_id + item_name
    item_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    todo_collection.insert_one({
        "item_id": item_id,
        "item_name": item_name,
        "item_description": item_description,
        "due_date": due_date,
        "priority": priority,
        "category": category,
        "item_uuid": item_uuid,
        "item_hash": item_hash
    })

    return f"""
    ✅ To-Do Item Submitted!<br>
    ID: {item_id}<br>
    UUID: {item_uuid}<br>
    Hash: {item_hash}<br>
    Name: {item_name}<br>
    Description: {item_description}<br>
    Due Date: {due_date}<br>
    Priority: {priority}<br>
    Category: {category}
    """


if __name__ == '__main__':
    app.run(debug=True)
