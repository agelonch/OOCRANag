from keystoneauth1.identity import v3
from keystoneauth1 import session
import sys


def auth(operator):
    try:
        auth = v3.Password(user_id=operator.id_user,
                           password='odissey09',
                           project_id=operator.id_project,
                           auth_url=operator.end_keystone)

        sess = session.Session(auth=auth)
        token = auth.get_token(sess)

        print "INFO: Authentification succesfully."
    except:
        print "INFO: Authentification failed."
        sys.exit(130)

    return token
