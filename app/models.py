from app import db

class User(db.Model):
	__tablename__ = 'info'
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
	username = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	email = db.Column(db.String(255), unique=True)

	def __init__(self, id, username, password, email):
		self.id = id
		self.username = username
		self.password = password
		self.email = email

	def __repr__(self):
		return "username : %s, password : %s, email : %s" % (self.username, self.password, self.email)

	def as_dict(self):
		return {x.name: getattr(self, x.name) for x in self.__table__.columns}