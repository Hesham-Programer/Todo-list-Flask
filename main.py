from flask import Flask, request, render_template, redirect, url_for
import datetime

now = datetime.datetime.now()
formatted_time = now.strftime("%h:%H:%M:%S")

todos = []
completed_todos = []

app = Flask(__name__, template_folder="templates")


@app.route(rule="/", methods=["GET", "POST"])
def home():
    global todos
    global completed_todos
    global formatted_time
    if request.method == "POST":
        if "completed" in request.form:
            return redirect(url_for("completed_tasks"))

        if "edit" in request.form:
            edit_todo = request.form.get("edit")
            return redirect(url_for("edit", todo=edit_todo))

        if "add" in request.form:
            todo_input = request.form.get("todo-input")
            add(todo=todo_input)

        if "delete" in request.form:
            todo = request.form.get("delete")
            delete(todo=todo)

        if "done" in request.form:
            checked_todo = request.form.get("done")
            complete_todo(todo_name=checked_todo)
            print(completed_todos)

    return render_template(template_name_or_list="index.html", todos=todos, redirect=redirect, url_for=url_for, delete=delete,)


@app.route(rule="/completed", methods=["GET", "POST"])
def completed_tasks():
    global formatted_time
    global completed_todos
    global todos
    if request.method == "POST":

        if "home" in request.form:
            return redirect(url_for("home"))

        if "done" in request.form:
            todo = request.form.get("done")
            undo(todo)

    return render_template(template_name_or_list="completed_todos.html", completed_todos=completed_todos, formatted_time=formatted_time,)

@app.route(rule="/edit/<todo>", methods=["GET", "POST"])
def edit(todo):
    global todos
    old_todo = todo
    if request.method == "POST":
        new_todo = request.form.get("edited-todo")

        if "ok" in request.form:
            todos[todos.index(old_todo)] = new_todo
            return redirect(url_for("home"))

    return render_template(template_name_or_list="edit.html", todo=todo)

def delete(todo):
    global todos
    del todos[todos.index(todo)]


def add(todo):
    global todos
    if todo == "":
        pass
    else:
        todos.append(todo)


def complete_todo(todo_name):
    global completed_todos
    completed_todos.append(todo_name)
    delete(todo_name)


def undo(todo_name):
    global todos
    global completed_todos
    todos.append(todo_name)
    del completed_todos[completed_todos.index(todo_name)]


if __name__ == '__main__':
    app.run(debug=True)
