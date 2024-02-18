from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)



@app.route('/')
def index():
	favourite_pizza =['Pepperoni', 'Cheese', 'Mushrooms', 42]
	return render_template('index.html', favourite_pizza=favourite_pizza)


#vad är det för connection? name i route och name i user måste vara sammankopplade, kolla på user.html
@app.route('/user/<name>')
def user(name):
	# i return kallar vi på name som name för att vi ska kunnna använda på html
	return render_template('user.html', name=name)


# Invalid url
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# Internal server error
@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500


if __name__=='__main__':
	app.run(debug=True)