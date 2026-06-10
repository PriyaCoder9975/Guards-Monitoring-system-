from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Table
class Guard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    shift = db.Column(db.String(50))
    location = db.Column(db.String(100))
    status = db.Column(db.String(50))

# Home Page
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Guard Monitoring System</title>
<style>
body{
font-family:Arial;
margin:40px;
background:#f4f4f4;
}
.container{
background:white;
padding:20px;
border-radius:10px;
}
table{
width:100%;
border-collapse:collapse;
}
table,th,td{
border:1px solid black;
padding:10px;
}
input{
padding:8px;
margin:5px;
}
button{
padding:10px;
background:green;
color:white;
border:none;
}
</style>
</head>
<body>
<div class="container">
<h1>Guard Monitoring System</h1>

<form method="POST" action="/add">
<input type="text" name="name" placeholder="Guard Name" required>
<input type="text" name="shift" placeholder="Shift" required>
<input type="text" name="location" placeholder="Location" required>
<input type="text" name="status" placeholder="Status" required>
<button type="submit">Add Guard</button>
</form>

<br>

<table>
<tr>
<th>ID</th>
<th>Name</th>
<th>Shift</th>
<th>Location</th>
<th>Status</th>
<th>Action</th>
</tr>

{% for guard in guards %}
<tr>
<td>{{ guard.id }}</td>
<td>{{ guard.name }}</td>
<td>{{ guard.shift }}</td>
<td>{{ guard.location }}</td>
<td>{{ guard.status }}</td>
<td>
<a href="/delete/{{ guard.id }}">Delete</a>
</td>
</tr>
{% endfor %}

</table>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    guards = Guard.query.all()
    return render_template_string(HTML, guards=guards)

@app.route('/add', methods=['POST'])
def add():
    guard = Guard(
        name=request.form['name'],
        shift=request.form['shift'],
        location=request.form['location'],
        status=request.form['status']
    )
    db.session.add(guard)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    guard = Guard.query.get(id)
    db.session.delete(guard)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
