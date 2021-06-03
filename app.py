from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class members(db.Model):
   id = db.Column('member_id', db.Integer, primary_key = True)
   name = db.Column(db.String(50))
   email = db.Column(db.String(30))
   dept = db.Column(db.String(30))

   def __init__(self, name, email, dept):
    self.name = name
    self.email = email
    self.dept = dept

@app.route('/')
def show_all():
   return render_template('show_all.html', members = members.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['email'] or not request.form['dept']:
         flash('Please enter all the fields', 'error')
      else:
         member = members(request.form['name'], request.form['email'], request.form['dept'])
         db.session.add(member)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

if __name__ == '__main__':
   db.create_all()
   app.run(host = '0.0.0.0')

