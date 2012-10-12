import cgi
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

FACEBOOK_APP_ID = '110626275752351'
FACEBOOK_APP_SECRET = 'a6d52ed9f11260e72c70b0c5432266f3'

app = Flask(__name__)
app.config['SECURITY_POST_LOGIN'] = '/profile' #REDIRECT
app.config['SOCIAL_FACEBOOK'] = {
    'oauth': {
        'consumer_key': '110626275752351',
        'consumer_secret': 'a6d52ed9f11260e72c70b0c5432266f3',
        'request_token_params': {
            'scope': 'email'
        }
    }
}
app.config['SOCIAL_CONNECT_ALLOW_REDIRECT'] = "localhost:5000/profile"
app.config['SECRET_KEY'] = "foobarbazblah"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
db = SQLAlchemy(app)
Security(app, SQLAlchemyUserDatastore(db))
Social(app, SQLAlchemyConnectionDatastore(db))

@app.before_first_request
def before_first_request():
    db.create_all()
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', content='Profile Page',
            facebook_conn=current_app.social.facebook.get_connection())


@app.route('/login')
def getUser():
  user = facebook.get_user_from_cookie(request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
  resp = make_response()
  if user:
    resp.data = user
    # Make calls  to db to find info and return
    # return user_details
    #return user['uid']
    return resp
  else:
    args = dict(client_id=FACEBOOK_APP_ID,
        redirect_uri=request.url_root+'loggedin')
    #url = facebook.auth_url(FACEBOOK_APP_ID, request.url)
    return redirect(
        "https://graph.facebook.com/oauth/authorize?" +
        urllib.urlencode(args))

@app.route('/loggedin')
def getUserFromFB():
  verification_code = request.args["code"]
  response = make_response()
  args = dict(client_id=FACEBOOK_APP_ID)
        #redirect_uri=request.url_root+'login')
  if request.args["code"]:
    args["client_secret"] = FACEBOOK_APP_SECRET
    args["code"] = request.args['code']
    x = cgi.parse_qs(urllib.urlopen(
      "https://graph.facebook.com/oauth/access_token?" +
      urllib.urlencode(args)).read())
    access_token = x["access_token"][-1]
    # Download the user profile and cache a local instance of the
    # basic profile info
    profile = json.load(urllib.urlopen(
      "https://graph.facebook.com/me?" +
      urllib.urlencode(dict(access_token=access_token))))
    user = User(key_name=str(profile["id"]), id=str(profile["id"]),
      name=profile["name"], access_token=access_token,
      profile_url=profile["link"])
    user.put()
    set_cookie(response, "fb_user", str(profile["id"]),
                         expires=time.time() + 30 * 86400)
    return "Logged in"

def set_cookie(response, name, value, domain=None, path="/", expires=None):
  """Generates and signs a cookie for the give name/value"""
  timestamp = str(int(time.time()))
  value = base64.b64encode(value)
  signature = cookie_signature(value, timestamp)
  cookie = Cookie.BaseCookie()
  cookie[name] = "|".join([value, timestamp, signature])
  cookie[name]["path"] = path
  if domain:
    cookie[name]["domain"] = domain
  if expires:
    cookie[name]["expires"] = email.utils.formatdate(
      expires, localtime=False, usegmt=True)
  response.headers._headers.append(("Set-Cookie", cookie.output()[12:]))


def parse_cookie(value):
  """Parses and verifies a cookie value from set_cookie"""
  if not value:
    return None
  parts = value.split("|")
  if len(parts) != 3:
    return None
  if cookie_signature(parts[0], parts[1]) != parts[2]:
    logging.warning("Invalid cookie signature %r", value)
    return None
  timestamp = int(parts[1])
  if timestamp < time.time() - 30 * 86400:
    logging.warning("Expired cookie %r", value)
    return None
  try:
    return base64.b64decode(parts[0]).strip()
  except:
    return None

def cookie_signature(*parts):
  """Generates a cookie signature.
  We use the Facebook app secret since it is different for every app (so
  people using this example don't accidentally all use the same secret).
  """
  hash = hmac.new(FACEBOOK_APP_SECRET, digestmod=hashlib.sha1)
  for part in parts:
    hash.update(part)
  return hash.hexdigest()


if __name__ == '__main__':
  app.run(debug=True, host = "0.0.0.0")
