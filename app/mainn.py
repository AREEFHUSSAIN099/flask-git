from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import uuid
import hashlib
import os
import json

app = Flask(__name__)

# ✅ MongoDB connection
client = MongoClient("mongodb+srv://areefhussain099:38013801areef@cluster099.ny6vqpr.mongodb.net/")
db = client["flask_db"]
collection = db["users"]
todo_collection = db["todo_items"]
todos_collection = db["todos"]

# ✅ Route for todo.html
@app.route('/')
@app.route('/todo')
def todo_form():
    return render_template('todo.html')

# ✅ To-Do submission with UUID and Hash
@app.route('/submit', methods=['POST'])
def submit_todo_item():
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')

    todo_id = str(uuid.uuid4())
    hash_input = title + description
    todo_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    todo_item = {
        'id': todo_id,
        'title': title,
        'description': description,
        'category': category,
        'hash': todo_hash
    }

    todos_collection.insert_one(todo_item)
    return redirect('/displaytodos')

# ✅ Display To-Do items page
@app.route('/displaytodos')
def display_todos():
    todos = list(todos_collection.find())
    return render_template('displaytodos.html', todos=todos)

# ✅ JSON route
@app.route('/jsondata')
def json_data():
    json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(json_path) as f:
        data = json.load(f)
    return data

# ✅ Alternate To-Do submission (old format)
@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item_old():
    item_id = request.form['itemId']
    item_name = request.form['itemName']
    item_description = request.form['itemDescription']
    due_date = request.form['dueDate']
    priority = request.form['priority']

    todo_collection.insert_one({
        "item_id": item_id,
        "item_name": item_name,
        "item_description": item_description,
        "due_date": due_date,
        "priority": priority
    })
    return f"✅ To-Do Item submitted! ID: {item_id}, Name: {item_name}, Description: {item_description}, Due Date: {due_date}, Priority: {priority}"

if __name__ == '__main__':
    app.run(debug=True)
