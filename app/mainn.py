from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import uuid
import hashlib  # ✅ NEW import

app = Flask(__name__)

# ✅ MongoDB connection
client = MongoClient("mongodb+srv://areefhussain099:3838areef@cluster099.ny6vqpr.mongodb.net/")
db = client["flask_db"]
todos_collection = db["todos"]

@app.route('/')
@app.route('/todo')  # ✅ Added /todo route
def todo_form():
    return render_template('todo.html')

@app.route('/submit', methods=['POST'])
def submit_todo_item():
    title = request.form['title']
    description = request.form['description']
    category = request.form['category']

    todo_id = str(uuid.uuid4())

    # ✅ NEW: Generate hash from title + description
    hash_input = title + description
    todo_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    todo_item = {
        'id': todo_id,
        'title': title,
        'description': description,
        'category': category,
        'hash': todo_hash  # ✅ NEW field
    }

    todos_collection.insert_one(todo_item)
    return redirect('/displaytodos')

@app.route('/displaytodos')
def display_todos():
    todos = list(todos_collection.find())
    return render_template('displaytodos.html', todos=todos)

if __name__ == '__main__':
    app.run(debug=True)
