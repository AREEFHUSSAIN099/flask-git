from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import uuid
import hashlib
import os
import json

app = Flask(__name__)

# ✅ MongoDB connection
client = MongoClient("mongodb+srv://areefhussain0:your_passwordareef@cluster099.ny6vqpr.mongodb.net/")
db = client["flask_db"]
todo_collection = db["todo_items"]

# ✅ Route: To-Do Form
@app.route('/')
@app.route('/todo')
def todo_form():
    return render_template('todo.html')

# ✅ Route: To-Do Form Submission
@app.route('/submit', methods=['POST'])
def submit_todo_item():
    title = request.form['title']
    description = request.form['description']
    category = request.form['category']

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

    todo_collection.insert_one(todo_item)
    return redirect('/displaytodos')

# ✅ Route: Display All To-Do Items
@app.route('/displaytodos')
def display_todos():
    todos = list(todo_collection.find())
    return render_template('displaytodos.html', todos=todos)

# ✅ Route: Serve JSON data from local file
@app.route('/jsondata')
def json_data():
    json_path = os.path.join(os.path.dirname(__file__), 'adata.json')
    with open(json_path) as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    app.run(debug=True)
