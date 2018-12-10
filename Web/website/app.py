from flask import Flask, Response, render_template, request, jsonify, redirect, url_for, session, make_response
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from models import db, Account, KeyboardMapping
from Crypto.Cipher import AES
from Crypto import Random
import sys, random, hashlib, re, binascii, os, json, uuid

LOCAL_TESTING = True

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = b'jf(JE|[1\29jIe|9|31$m_z=+1,f3<1AFg.'
app.debug = True
# Postgres Database
if LOCAL_TESTING:
	POSTGRES = {
	    'user': 'mwornow',
	    'pw': 'password',
	    'db': 'hardpass',
	    'host': 'localhost',
	    'port': '5432',
	}
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vzqjcmqrxntjfm:beeef99596aec71949988ccef4916093e73a78463849c91a43383997b617b352@ec2-54-227-249-201.compute-1.amazonaws.com:5432/df9iusvct4hb1'
	#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
	
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)




#
#
# WEBPAGES
#
#

@app.route("/", methods = ['GET'])
def index():
	return render_template("index.html")

@app.route("/features", methods = ['GET'])
def features():
	return render_template("features.html")

@app.route("/home", methods = ['GET'])
def home():
	# (1) Get logged in user info
	user_id = session['user_id'] if 'user_id' in session else None
	if user_id is None:
		return redirect(url_for("index"))

	# (2) Get user's keyboard mappings
	keyboard_mappings = KeyboardMapping.query.filter_by(user_id = user_id)
	mappings = []
	for km in keyboard_mappings:
		# ## Decrypt mapping
		# iv = m.iv.encode()
		# key = hashlib.sha256(session['user_token'].encode('utf-8')).digest()
		# encryption_suite = AES.new(key, AES.MODE_CFB, iv)
		# m.mapping_decrypted = json.loads(encryption_suite.decrypt(m.mapping))
		mappings.append(json.loads(km.mapping))
	return render_template("home.html", keyboard_mappings = keyboard_mappings, mappings = mappings)


@app.route("/login", methods = ['GET', 'POST'])
def login():
	if request.method == "POST":
		# (1) Get input
		email = request.form['email'] if 'email' in request.form else None
		password = request.form['password'] if 'password' in request.form else None
		
		# (2) Get user
		user = Account.query.filter_by(email=email).first()
		if user is None:
			## No user exists with this email
			return render_template('login.html', error = True, code = 1, errorMsg = "Invalid email")

		# (3) Validate user
		## Hash input password with user's salt
		hashed_password = hashlib.sha256((password + user.salt).encode('utf-8')).hexdigest()
		if hashed_password != user.password:
			## Invalid password
			return render_template('login.html', error = True, code = 2, errorMsg = "Invalid password")
		else:
			## Succesfully logged user in
			session['user_id'] = user.id
			session['user_email'] = user.email
			session['user_token'] = user.token
			## Set cookie for future async mapping requests
			response = make_response(redirect(url_for('home')))
			response.set_cookie('user_token', user.token)
			return response
	else:
		return render_template("login.html")


@app.route("/login_extension", methods = ['POST'])
def login_extension():
	result = {}
	result['error'] = 0 # Success = 0

	# (1) Get input
	email = request.form['email'] if 'email' in request.form else None
	password = request.form['password'] if 'password' in request.form else None
	
	# (2) Get user
	user = Account.query.filter_by(email=email).first()
	if user is None:
		## No user exists with this email
		result['error'] = 1
		result['errorMsg'] = 'Invalid email'
		return jsonify(result)

	# (3) Validate user
	## Hash input password with user's salt
	hashed_password = hashlib.sha256((password + user.salt).encode('utf-8')).hexdigest()
	if hashed_password != user.password:
		## Invalid password
		result['error'] = 2
		result['errorMsg'] = 'Invalid password'
		return jsonify(result)
	else:
		## Succesfully logged user in
		result['token'] = user.token
		return jsonify(result)


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
	if request.method == "POST":
		result = {}
		result['error'] = 0 # Error code 0 = success

		# (1) Get input
		email = request.form['email'] if 'email' in request.form else None
		password = request.form['password'] if 'password' in request.form else None
		confirmpassword = request.form['confirmpassword'] if 'confirmpassword' in request.form else None
		
		# (2) Check that required input is there
		if email is None or password is None or confirmpassword is None:
			## Invalid input
			return render_template('signup.html', error = True, code = 1, errorMsg = 'Invalid form input')

		# (3) Validate input
		## Email
		invalidEmail = not re.match(r'[^@]+@[^@]+\.[^@]+', email)
		invalidUniqueEmail = Account.query.filter_by(email = email).count() > 0
		## Password
		invalidPassword = not (len(password) > 0)
		invalidPasswordMatch = not (password == confirmpassword)
		if invalidEmail or invalidUniqueEmail or invalidPassword or invalidPasswordMatch:
			errorMsgs = []
			if invalidEmail: errorMsgs.append('Invalid email')
			if invalidUniqueEmail: errorMsgs.append('Email address already taken by another user')
			if invalidPassword: errorMsgs.append('Invalid password')
			if invalidPasswordMatch: errorMsgs.append('Passwords did not match')
			errorMsg = ', '.join(errorMsgs)
			return render_template('signup.html', error = True, code = 2, errorMsg = errorMsg)

		# (4) Create account for user
		token = str(binascii.b2a_hex(os.urandom(64)), 'utf-8')
		salt = str(binascii.b2a_hex(os.urandom(64)), 'utf-8')
		hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
		new_user_obj = Account(email, hashed_password, salt, token)

		try:
			db.session.add(new_user_obj)
			db.session.commit()
			return redirect(url_for('login'))
		except Exception as e:
			### Error creating account
			db.session.rollback()
			db.session.flush()
			### Return error to user
			print(str(e))
			return render_template('signup.html', error = True, code = 4, errorMsg = 'Error creating account in database')
	else:
		return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))

#
#
# BACKEND KEYBOARD MAPPING
#
#


def generateMapping():
	# Crypto secure random number generator based on OS
	rng = random.SystemRandom()
	# Dictionary mapping 1 char -> sequence of 3-4 random chars
	mapping = {}
	# Valid keyboard chars are any ASCII char code from [32, 126] inclusive
	valid_ascii_char_codes = range(32, 127)
	valid_mapping_lengths = [3,4]
	for i in valid_ascii_char_codes:
		char = chr(i)
		## Generate random string of 3-4 chars
		mapping_length = rng.choice(valid_mapping_lengths)
		mapping_chars = [ chr(i) for i in rng.choices(valid_ascii_char_codes, k = mapping_length) ]
		## Map 'char' -> 'mapping_chars'
		mapping[char] = mapping_chars
	return mapping

@app.route("/get_mapping", methods = ['POST'])
def get_mapping():
	#
	# This POST request is sent when the user focuses onto a password field on a web page
	# It either:
	#		(1) If a current mapping for this webpage exists, return that existing mapping
	#		(2) If no mapping exists for this webpage, create a new one, save it to the DB, and return it to the user
	result = {}
	result['error'] = 0 # Error of 0 = success
	# (1) Get input
	website = request.form['website'] if 'website' in request.form else None
	token = request.form['token'] if 'token' in request.form else None
	# (2) Check that required input is there
	if website is None or token is None:
		## Invalid input
		result['error'] = 1
		result['errorMsg'] = "Invalid input"
		return jsonify(result)
	# (3) Get user
	user = Account.query.filter_by(token=token).first()
	if user is None:
		## No user exists with ID user_id
		result['error'] = 2
		result['errorMsg'] = "No user"
		return jsonify(result)
	# (4) Get keyboard mapping
	mapping_obj = KeyboardMapping.query.filter_by(user_id = user.id, website = website).first()
	if mapping_obj is None:
		## No mapping currently exists
		## So, create one
		new_mapping = generateMapping()
		## Encrypt new_mapping with AES
		# ### Key = user's password, IV = random 256 char string
		# iv = hashlib.sha256(token.encode('utf-8')).digest()
		# key = hashlib.sha256(token.encode('utf-8')).digest()
		# encryption_suite = AES.new(key, AES.MODE_CFB, iv)
		# new_mapping_encrypted = encryption_suite.encrypt(json.dumps(new_mapping))
		iv = uuid.uuid4().hex
		mapping_encoded = json.dumps(new_mapping)
		print(mapping_encoded)
		new_mapping_obj = KeyboardMapping(user.id, mapping_encoded, website, iv)

		## Save mapping in database
		try:
			db.session.add(new_mapping_obj)
			db.session.commit()
			## Return mapping to user
			result['mapping'] = new_mapping
			return jsonify(result)
		except Exception as e:
			### Error saving mapping in database
			print(str(e))
			db.session.rollback()
			db.session.flush()
			### Return error to user
			result['error'] = 4
			result['errorMsg'] = "Error creating mapping"
			return jsonify(result)
	else:
		## Decrypt existing password with AES
		# iv = mapping_obj.iv
		# key = hashlib.sha256(token.encode('utf-8')).digest()
		# encryption_suite = AES.new(key, AES.MODE_CFB, iv)
		# mapping_decrypted = json.loads(encryption_suite.decrypt(mapping_obj.mapping))
		mapping_decoded = json.loads(mapping_obj.mapping)
		## Return existing mapping to user
		result['mapping'] = mapping_decoded
		return jsonify(result)


if __name__ == '__main__':
	app.run(debug=True,
			port=5000)