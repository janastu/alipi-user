from flask import Flask
from flask import request
from flask import url_for
from flask import make_response
from flask import redirect
from flask import render_template
from flask import current_app
from flask import request
import urllib
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.social import Social
from flask.ext.security import (Security, LoginForm)
from flask.ext.social.datastore.sqlalchemy import SQLAlchemyConnectionDatastore
from flask.ext.security.datastore.sqlalchemy import SQLAlchemyUserDatastore
from flask.ext.login import login_required
from flask.ext.social import FacebookLoginHandler
# import facebook


app = Flask(__name__)
app.config['SECURITY_POST_LOGIN'] = '/profile' #REDIRECT
db = SQLAlchemy(app)
Security(app, SQLAlchemyUserDatastore(db))
Social(app, SQLAlchemyConnectionDatastore(db))
app.config['SOCIAL_FACEBOOK'] = {
    'oauth': {
        'consumer_key': '110626275752351',
        'consumer_secret': 'a6d52ed9f11260e72c70b0c5432266f3',
        'request_token_params': {
            'scope': 'email'
        }
    }
}
app.config['SECRET_KEY'] ="foobarbazblah"
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', content='Profile Page',
            facebook_conn=current_app.social.facebook.get_connection())


@app.route('/login')
def login():
    return render_template('login.html', content='Login Page',login_form=LoginForm())

 # @app.route('/login/facebook')
# def ():
#     return repr(request)


if  __name__ == '__main__':
  app.run(debug=True)
