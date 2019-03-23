from flask import Flask,render_template,url_for,redirect,request,session
from models.models import user_exists,create_user,login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'

@app.route('/')
def home():

	return render_template('home.html',name = 'kavya',title = 'home', home = 'home')



@app.route('/about')
def about_me():

	return render_template('about.html',title = 'about')

@app.route('/contact')
def contact():

	return render_template('contact.html',title = 'contact')

@app.route('/welcome')
def  welcome():

	return render_template('welcome.html')

@app.route('/login',methods = ['POST','GET'])
def login():

	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		user = login_user(username)



		if user is None:
			return "this user doesnot exist"

		if user['username'] == username:
			if user['password'] == password:
				session['username'] = username
				session['c_type'] = user['c_type']
				return redirect(url_for('home'))
			return "wrong password, go back and try again!"
	

	else:

		return redirect(url_for('home'))

@app.route('/signup',methods = ['POST','GET'])

def signup():

	if request.method == 'POST':

		user_info = {}

		user_info['username'] = request.form['username']
		user_info['email'] = request.form['email']
		user_info['password'] = request.form['password']
		user_info['c_type'] = request.form['c_type']
		rpassword = request.form['rpassword']


		if user_exists(user_info['username']) is False:
			if user_info['password'] == rpassword:
				if user_info['c_type'] == 'buyer':
					user_info['cart'] = []
				create_user(user_info)
				return render_template('welcome.html',user = user_info['username'])
			return "password do not match. Re-enter password correctly "
		return "user exists already. Enter another username"



	else:

		return redirect(url_for('home'))	

@app.route('/logout')
def logout():

	session.clear()
	return redirect(url_for('home'))


if __name__ == '__main__':

	app.run(debug = True)


