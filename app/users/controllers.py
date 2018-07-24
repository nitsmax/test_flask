import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g
from flask import current_app as app
from app.commons import build_response
from app.users.models import User
from app.auth.models import login_required
from app.commons.utils import update_document
from werkzeug.security import generate_password_hash, check_password_hash


users = Blueprint('users_blueprint', __name__,
                    url_prefix='/api/users')


@users.route('', methods=['POST'])
def create_user():
    """
    Create a story from the provided json
    :param json:
    :return:
    """
    content = request.get_json(silent=True)

    user = User()
    user.firstName = content.get("firstName")
    user.lastName = content.get("lastName")
    user.email = content.get("email")
    user.password = generate_password_hash(content.get("password"))
    
    try:
        user_id = user.save()
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    return build_response.build_json({
        "_id": str(user_id.id)
    })


@users.route('')
@login_required
def read_users():
    print(g.user.email)
    """
    find list of intents for the agent
    :return:
    """
    users = User.objects().order_by('lastName')
    return build_response.sent_json(users.to_json())


@users.route('/<id>')
def read_intent(id):
    """
    Find details for the given intent id
    :param id:
    :return:
    """
    return Response(response=dumps(
        Intent.objects.get(
            id=ObjectId(
                id)).to_mongo().to_dict()),
        status=200,
        mimetype="application/json")


@users.route('/<id>', methods=['PUT'])
def update_intent(id):
    """
    Update a story from the provided json
    :param intent_id:
    :param json:
    :return:
    """
    json_data = loads(request.get_data())
    intent = Intent.objects.get(id=ObjectId(id))
    intent = update_document(intent, json_data)
    intent.save()
    return 'success', 200


@users.route('/<id>', methods=['DELETE'])
def delete_intent(id):
    """
    Delete a intent
    :param id:
    :return:
    """
    Intent.objects.get(id=ObjectId(id)).delete()

    try:
        train_models()
    except BaseException:
        pass

    # remove NER model for the deleted stoy
    try:
        os.remove("{}/{}.model".format(app.config["MODELS_DIR"], id))
    except OSError:
        pass
    return build_response.sent_ok()


from flask import send_file
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


@users.route('/export', methods=['GET'])
def export_intents():
    """
    Deserialize and export Mongoengines as jsonfile
    :return:
    """
    strIO = StringIO.StringIO()
    strIO.write(Intent.objects.to_json())
    strIO.seek(0)
    return send_file(strIO,
                     attachment_filename="iky_intents.json",
                     as_attachment=True)


from flask import abort
from bson.json_util import loads


@users.route('/import', methods=['POST'])
def import_intents():
    """
    Convert json files to Intents objects and insert to MongoDB
    :return:
    """
    # check if the post request has the file part
    if 'file' not in request.files:
        abort(400, 'No file part')
    json_file = request.files['file']
    intents = import_json(json_file)

    return build_response.build_json({"num_intents_created": len(intents)})


def import_json(json_file):
    json_data = json_file.read().decode('utf-8')
    # intents = Intent.objects.from_json(json_data)
    intents = loads(json_data)

    creates_intents = []
    for intent in intents:
        new_intent = Intent()
        new_intent = update_document(new_intent, intent)
        new_intent.save()
        creates_intents.append(new_intent)
    return creates_intents