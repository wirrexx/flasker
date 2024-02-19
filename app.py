from flask import Flask, render_template, request, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#add secret key!
app.config['SECRET_KEY'] = 'thisismysecretkey'

# initialize databasen
db = SQLAlchemy(app)


# skapa modellen, vad vill vi spara på db? CRUD
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

	# create a string
    def __repr__(self):
	    return f'Name {self.name}'

class UserForm(FlaskForm):
	name =  StringField("Name ", validators=[DataRequired()])
	email =  StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Submit")




# Create a formclass, kalla på en klass när vi kallar på den. validators vill ha något skrivet
class NamerForm(FlaskForm):
	name =  StringField("What's your name? ", validators=[DataRequired()])
	submit = SubmitField("Submit")


@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None: 
			user = Users(name=form.name.data, email=form.email.data)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data=''
		form.email.data=''
		flash('User Added Successfully!')
	our_users=Users.query.order_by(Users.date_added)
	return render_template('add_user.html', form=form, name=name, our_users=our_users)


@app.route('/')
def index():
	return render_template('index.html')


#vad är det för connection? name i route och name i user måste vara sammankopplade, kolla på user.html
@app.route('/user/<name>')
def user(name):
	# i return kallar vi på name som name för att vi ska kunnna använda på html
	return render_template('user.html', name=name)


# Invalid url
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


# Internal server error message
@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500


# Create name page
@app.route('/name', methods=['GET', 'POST'])
def create_name():
	name = None
	form = NamerForm()
	# validate form
	if form.validate_on_submit():		
		name = form.name.data
		form.name.data = ''
		flash('Form Submitted Successfully!')
	return render_template('name.html', name=name, form=form)


if __name__=='__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)	