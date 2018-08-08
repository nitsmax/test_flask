import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g, url_for
from flask import current_app as app
from app.commons import build_response
from app.emojis.models import Emoji, Category
from app.auth.models import login_required
from app.commons.utils import update_document
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


emojis = Blueprint('emojis_blueprint', __name__,
                    url_prefix='/api/emojis')

@emojis.route('/categories')
def get_categories():
    '''
    For inserting the categories
    '''
    '''categories = ['Bollywood', 'Hollywood', 'Modern']
    for cat in categories:
        category = Category()
        category.name = cat
        category.save()

    return build_response.sent_ok()
    '''
    categories = Category.objects().order_by('name')
    if not categories:
        return build_response.build_json([])
    #return build_response.sent_json(emojis.to_json())

    response_categories = []

    for category in categories:
        obj_category = {
            'id': str(category.id),
            'name': category.name,
            'date_created': category.date_created.isoformat(),
            'date_modified': category.date_modified.isoformat()
        }
        response_categories.append(obj_category)

    return build_response.build_json(response_categories)

@emojis.route('', methods=['POST'])
def create_emoji():
    """
    Create a story from the provided json
    :param json:
    :return:
    """
    emoji = Emoji()

    # check if the post request has the file part
    if 'Image' in request.files:
        imageDirectory = os.path.join(app.config.get('APP_ROOT'), 'static', 'uploads', 'emojis')
        file = request.files['Image']

        filename = secure_filename(file.filename)
        file.save(os.path.join(imageDirectory, filename))
        emoji.imagefile = filename

    if request.form.get("category"):
        category = Category.objects(name=request.form.get("category")).get()
        if category:
            emoji.category = category

    if request.form.get("tags"):
        tags_string = request.form.get("tags")
        tags = [x.strip() for x in tags_string.split(',')]   
        emoji.tags = tags

    if request.form['isPaid'].lower() == 'true':
        emoji.isPaid = True
    else:
        emoji.isPaid = False

    emoji.name = request.form['name']

    if request.form.get("description"):
        emoji.description = request.form['description']

    try:
        emoji_id = emoji.save()
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    return build_response.build_json({
        "_id": str(emoji_id.id)
    })


@emojis.route('')
#@login_required
def read_emojis():
    print(request.args.get('category'))
    """
    find list of emojis for the agent
    :return:
    """
    emojis = Emoji.objects()
    if request.args.get('name'):
        emojis = emojis.filter(name__iexact=request.args.get('name'))

    if request.args.get('category'):
        category = Category.objects(name__iexact=request.args.get('category')).get()
        emojis = emojis.filter(category=category)

    if request.args.get('q'):
        emojis = emojis.filter(tags__icontains=request.args.get('q'))

    if request.args.get('isPaid'):
        emojis = emojis.filter(isPaid=True) if request.args.get('isPaid').lower() == 'true' else emojis.filter(isPaid=False)


    #emojis.find()

    if not emojis:
        return build_response.build_json([])
    #return build_response.sent_json(emojis.to_json())

    response_emojis = []

    for emoji in emojis:
        obj_emoji = {
            'id': str(emoji.id),
            'name': emoji.name,
            'isPaid': emoji.isPaid,
            'tags': emoji.tags,
            'category' : emoji.category.name if emoji.category else '',
            'description': emoji.description,
            'image': '' if not emoji.imagefile else url_for('emojis_file', path=emoji.imagefile, _external=True),
            'date_created': emoji.date_created.isoformat(),
            'date_modified': emoji.date_modified.isoformat()
        }
        response_emojis.append(obj_emoji)

    return build_response.build_json(response_emojis)


@emojis.route('/<id>')
def read_emoji(id):
    """
    Find details for the given intent id
    :param id:
    :return:
    """
    return Response(response=dumps(
        Emoji.objects.get(
            id=ObjectId(
                id)).to_mongo().to_dict()),
        status=200,
        mimetype="application/json")


@emojis.route('/<id>', methods=['PUT'])
def update_emoji(id):
    """
    Update a story from the provided json
    :param intent_id:
    :param json:
    :return:
    """
    json_data = loads(request.get_data().decode('utf-8'))
    emoji = Emoji.objects.get(id=ObjectId(id))
    emoji = update_document(emoji, json_data)
    emoji_id.save()
    return 'success', 200


@emojis.route('/<id>', methods=['DELETE'])
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


@emojis.route('/export', methods=['GET'])
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


@emojis.route('/import', methods=['POST'])
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