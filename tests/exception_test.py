from core.libs.exceptions import FyleError

def test_exception():
  assert FyleError(200,'hello').to_dict() =={'message':'hello'}

