from flask import Flask
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy

application = Flask(__name__)
#test
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
application.config['DEBUG'] = True
db = SQLAlchemy(application)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

class Datapoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id))
    date = db.Column(db.Text)
    basal_temperature = db.Column(db.Text)
    days_since_period_began = db.Column(db.Integer)

db.create_all()

api_manager = APIManager(application, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Datapoints, methods=['GET', 'POST', 'DELETE', 'PUT'])

if __name__ == "__main__":
    application.run()