activate_this = '/home/nitesh/work/leloji/backend/venv_env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/nitesh/work/leloji/backend/")

from app import app as application
application.secret_key = 'nitesh123#'
