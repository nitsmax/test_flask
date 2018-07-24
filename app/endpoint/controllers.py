from bson import ObjectId
import json

from jinja2 import Template

from flask import Blueprint, request, abort
from app import app

from app.commons.logger import logger
from app.commons import build_response
from app.users.models import User

from app.endpoint.utils import get_synonyms, SilentUndefined, split_sentence, call_api

endpoint = Blueprint('api', __name__, url_prefix='/api')



# Request Handler
@endpoint.route('/v1', methods=['POST'])
def api():
    return abort(400)

