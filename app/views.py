from flask import render_template, request, Flask, redirect, url_for, session
from app import app, db, bcrypt
from app.models import User


@app.route('/main')
@app.route('/')
def main():
	return render_template('main.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		# bcrypt encrypt
		pw_hash = bcrypt.generate_password_hash(request.form['password'])
		user = User(request.form['username'], pw_hash, request.form['email'])
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('main'))

	return render_template('signup.html')

@app.route('/signin', methods=['POST', 'GET'])
def signin():
	if request.method == 'POST':
		un = request.form['username']
		pw = request.form['password']
		res = db.session.query(User).filter_by(username=un).first()
		if res and bcrypt.check_password_hash(res.password, pw):
			session['logged_in'] = True
			session['username'] = un
			return redirect(url_for('main'))
		else:
			return 'not'
	else:	
		return render_template('signin.html')


@app.route('/programs')
def programs():
	return render_template('programs.html')


@app.route('/info', methods=['POST', 'GET'])
def info():
	''' get information from db, show and update if needed '''
	un = session['username']
	user = db.session.query(User).filter_by(username=un).first()
	if request.method == 'POST':
		if request.form['up_username'] is not None:
			user.username = request.form['up_username']
			session['username'] = request.form['up_username']
		if request.form['up_password'] is not None:
			user.password  = request.form['up_password']
		db.session.commit()
		return redirect(url_for('main'))
	else:
		return render_template('info.html', username=user.username, password=user.password, email=user.email)


@app.route('/signout')
def signout():
	session['logged_in'] = False
	return render_template('main.html')