from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
import git


# gets name of the .py file so Flask knows it's name
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '7e78101c061bf50314f915edeca709ab'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), unique=True, nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   password = db.Column(db.String(60), nullable=False)

   def __repr__(self):
       return f"User('{self.username}', '{self.email}')"

with app.app_context():
   db.create_all()


# tells you the URL the method below is related to
@app.route("/")
@app.route("/home")
def hello_world():
   # prints HTML to the webpage
   return render_template('home.html', firstname = "Philana")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/demo2seo/mysite/seo_ses12')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")