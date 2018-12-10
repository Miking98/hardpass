from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(5000), unique = True)
	password = db.Column(db.String(5000))
	salt = db.Column(db.String(256))
	token = db.Column(db.String(256)) # Token that user's browser stores in cookies after successful login, for future login-less async mapping requests
	created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self, email, password, salt, token):
		self.email = email
		self.password = password
		self.salt = salt
		self.token = token

	def __repr__(self):
		return '<Email %r>' % self.email

class KeyboardMapping(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
	mapping = db.Column(db.Text, nullable = True) # Note: mapping is stored as an AES-encrypted JSON string which encodes a Python dictionary; the encryption is done with AES, where the user's password is a key and IV is in db.iv column
	website = db.Column(db.String(5000)) # Base URL of website, i.e. "google.com" in https://www.google.com
	iv = db.Column(db.String(256)) # IV for AES encryption of mapping
	created = db.Column(db.DateTime, server_default=db.func.now())
	updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
	
	def __init__(self, user_id, mapping, website, iv):
		self.user_id = user_id
		self.mapping = mapping
		self.website = website
		self.iv = iv

	def __repr__(self):
		return '<Website: %r>' % self.website