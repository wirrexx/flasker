from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismysecretkey'



# Create a formclass, kalla på en klass när vi kallar på den. validators vill ha något skrivet
class NamerForm(FlaskForm):
	name =  StringField("What's your name? ", validators=[DataRequired()])
	submit = SubmitField("Submit")




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
	return render_template('name.html', name=name, form=form)


if __name__=='__main__':
	app.run(debug=True)	