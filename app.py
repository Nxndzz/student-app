from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
VERSION = "v1"
students = []
next_id = 1

PAGE = """
<!doctype html>
<title>Student Management {{v}}</title>
<h2>Student Management ({{v}})</h2>

<form method="post" action="/add">
  <input name="name" placeholder="Name" required>
  <input name="course" placeholder="Course" required>
  <input name="email" placeholder="Email" required>
  <button>Add Student</button>
</form>
<br>
<table border="1" cellpadding="6">
  <tr><th>ID</th><th>Name</th><th>Course</th><th>Email</th></tr>
  {% for s in students %}
  <tr><td>{{s.id}}</td><td>{{s.name}}</td><td>{{s.course}}</td><td>{{s.email}}</td></tr>
  {% endfor %}
</table>
"""

@app.route("/")
def index():
    return render_template_string(PAGE, students=students, v=VERSION)

@app.route("/add", methods=["POST"])
def add():
    global next_id
    students.append({"id": next_id,
                     "name": request.form["name"],
                     "course": request.form["course"],
                     "email": request.form["email"]})
    next_id += 1
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)