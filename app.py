from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)
DB = "students.db"

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

with db() as c:
    c.execute("""CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, dept TEXT, email TEXT)""")

PAGE = """
<!doctype html><title>Student Management v2</title>
<style>body{font-family:Arial;margin:40px}
table{border-collapse:collapse;width:100%;margin-top:15px}
td,th{border:1px solid #ccc;padding:8px;text-align:left}
input{padding:6px;margin-right:6px}</style>
<h1>Student Management - v2</h1>    
<form method="post" action="/add">
  <input name="name" placeholder="Name" required>
  <input name="dept" placeholder="Department" required>
  <input name="email" placeholder="Email" required>
  <button>Add</button>
</form>
<table>
<tr><th>ID</th><th>Name</th><th>Department</th><th>Email</th><th>Actions</th></tr>
{% for s in students %}
<tr><td>{{s.id}}</td><td>{{s.name}}</td><td>{{s.dept}}</td><td>{{s.email}}</td>
<td><a href="/edit/{{s.id}}">Edit</a>
<form method="post" action="/delete/{{s.id}}" style="display:inline"><button>Delete</button></form></td></tr>
{% endfor %}
</table>
"""

@app.route("/")
def index():
    rows = db().execute("SELECT * FROM students").fetchall()
    return render_template_string(PAGE, students=rows)

@app.route("/add", methods=["POST"])
def add():
    with db() as c:
        c.execute("INSERT INTO students(name,dept,email) VALUES(?,?,?)",
                  (request.form["name"], request.form["dept"], request.form["email"]))
    return redirect("/")

EDIT = """
<!doctype html><title>Edit Student</title>
<body style="font-family:Arial;margin:40px">
<h2>Edit student #{{s.id}}</h2>
<form method="post">
  <input name="name" value="{{s.name}}" required>
  <input name="dept" value="{{s.dept}}" required>
  <input name="email" value="{{s.email}}" required>
  <button>Save</button> <a href="/">Cancel</a>
</form></body>
"""

@app.route("/edit/<int:sid>", methods=["GET", "POST"])
def edit(sid):
    if request.method == "POST":
        with db() as c:
            c.execute("UPDATE students SET name=?, dept=?, email=? WHERE id=?",
                      (request.form["name"], request.form["dept"], request.form["email"], sid))
        return redirect("/")
    s = db().execute("SELECT * FROM students WHERE id=?", (sid,)).fetchone()
    return render_template_string(EDIT, s=s)

@app.route("/delete/<int:sid>", methods=["POST"])
def delete(sid):
    with db() as c:
        c.execute("DELETE FROM students WHERE id=?", (sid,))
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)