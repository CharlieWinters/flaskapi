from flask import Flask, request, Response
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import current_user, UserMixin, LoginManager
from flask.ext.restless import ProcessingException


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
app.config['DEBUG'] = True

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

class User(UserMixin):
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        Flask.flash('Logged in successfully.')

        next = Flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return Flask.abort(400)

        return Flask.redirect(next or flask.url_for('index'))
    return Flask.render_template('login.html', form=form)


class Datapoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id))
    date = db.Column(db.Text)
    basal_temperature = db.Column(db.Text)
    days_since_period_began = db.Column(db.Integer)

def auth_func(*args, **kwargs):
    if not current_user.is_authenticated():
        raise ProcessingException(description='Not authenticated!', code=401)
    return True

db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Datapoints, methods=['GET', 'POST', 'DELETE', 'PUT'],preprocessors=dict(GET_MANY=[auth_func]))


if __name__ == "__main__":
    app.run()