from quafelweb.admin.account import authenticate

def require_auth(fn):

  auth : authenticate.BaseAuthenticator = authenticate.BaseAuthenticator.GetInstance("kitopenid")

  def _deco(req):
    if auth.is_logged_in(req):
      
      return fn(req)
    else:
      auth.authenticate_view(req)

  return _deco