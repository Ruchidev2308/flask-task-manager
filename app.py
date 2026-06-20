from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

FILE_NAME = "tasks.json"

# ==========================================
# LECTURE 7: FILE I/O OPERATIONS
# ==========================================

def load_tasks():
    """Reads tasks from a file using File I/O. Returns a list."""
    # If the file does not exist yet, return a default starting list
    if not os.path.exists(FILE_NAME):
        return [{"id": 1, "task": "Learn Flask Basics", "done": False}]
    
    # Open and read the file ('r' mode)
    with open(FILE_NAME, "r") as file:
        return json.load(file)

def save_tasks(tasks_list):
    """Writes the updated tasks list back to the file ('w' mode)."""
    with open(FILE_NAME, "w") as file:
        json.dump(tasks_list, file, indent=4)


# ==========================================
# FLASK WEB ROUTES & LOGIC
# ==========================================

@app.route('/')
def index():
    # Load tasks fresh from the text file every time someone visits the page
    todos = load_tasks()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task_text = request.form.get('task')
    if task_text:
        todos = load_tasks()
        new_id = len(todos) + 1 if todos else 1
        
        # New tasks always start with "done": False
        todos.append({"id": new_id, "task": task_text, "done": False})
        
        save_tasks(todos)
    return redirect(url_for('index'))

# NEW ROUTE: Marks a task as complete/incomplete using Python Conditionals
@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    todos = load_tasks()
    
    # Loop through the list to find the matching task ID
    for item in todos:
        if item['id'] == todo_id:
            # LECTURE 2 CONDITIONALS: Toggle the boolean value
            if item['done'] is True:
                item['done'] = False
            else:
                item['done'] = True
            break # Exit the loop once found
            
    save_tasks(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    todos = load_tasks()
    # Filter out the item to delete
    todos = [t for t in todos if t['id'] != todo_id]
    save_tasks(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
