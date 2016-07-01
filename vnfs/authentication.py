from keystoneclient.auth.identity import v2 as identity
from keystoneclient import session
import sys

def auth(name):
  try:
    auth = identity.Password(auth_url="http://controller:5000/v2.0/",
                             username=name,
                             password="odissey09",
                             tenant_name=name)

    sess = session.Session(auth=auth)
    token = auth.get_token(sess)
    print "INFO: Authentification succesfully."
  except:
    print "INFO: Authentification failed."
    sys.exit(130)

  return token