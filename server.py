from flask import Flask
from flask import request
from flask import url_for
from flask import make_response
from flask import redirect
import urllib
import facebook

FACEBOOK_APP_ID = '404415776289287'
FACEBOOK_APP_SECRET = "98047be5a3ba4477121d79cc07e71882"

app = Flask(__name__)

@app.route('/login')
def getUser():
  user = facebook.get_user_from_cookie(request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
  resp = make_response()
  #resp.headers['Connection'] = 'keep-alive'
  if user:
    # Make calls  to db to find info and return
    # return user_details
    return user['uid']
  else:
    args = dict(client_id=FACEBOOK_APP_ID,
        redirect_uri=request.url)
    #url = facebook.auth_url(FACEBOOK_APP_ID, request.url)
    return redirect(
        "https://graph.facebook.com/oauth/authorize?" +
        urllib.urlencode(args))

    #return url
    #graph = facebook.GraphAPI(user["access_token"])
    #friends = graph.get_connections("me", "friends")
    #profile = graph.get_object("me")
    #res = []
    #res.append(profile)
    #res.append(friends)
    #resp.data = res 
    #return resp
  #else:
  #  return 

#def getUserFromFB():
if __name__ == '__main__':
  app.run(debug=True)
