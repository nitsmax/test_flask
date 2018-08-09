import os
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g
from flask import current_app as app
from app.commons import build_response
from app.emojis.models import Emoji, Category
from app.auth.models import login_required
from app.emojis.tasks import save_emoji, transpose_emoji


emojis = Blueprint('emojis_blueprint', __name__,
                    url_prefix='/api/emojis')

@emojis.route('/categories')
def get_categories():
    '''
    For inserting the categories
    '''
    categories = ['Bollywood', 'Hollywood', 'Modern']
    for cat in categories:
        category = Category()
        category.name = cat
        category.save()

    return build_response.sent_ok()
    
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
    try:
        save_response = save_emoji(emoji)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({
                "_id": str(save_response['emoji_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})

@emojis.route('')
#@login_required
def read_emojis():
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


    if not emojis:
        return build_response.build_json([])

    response_emojis = []

    for emoji in emojis:
        obj_emoji = transpose_emoji(emoji)
        response_emojis.append(obj_emoji)

    return build_response.build_json(response_emojis)


@emojis.route('/<id>')
def read_emoji(id):
    """
    Find details for the given emoji id
    :param id:
    :return:
    """
    try:
        emoji = Emoji.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    return build_response.build_json(transpose_emoji(emoji))


@emojis.route('/<id>', methods=['PUT'])
def update_emoji(id):
    emoji = Emoji.objects.get(id=ObjectId(id))
    try:
        save_response = save_emoji(emoji)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({
                "_id": str(save_response['emoji_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})



@emojis.route('/<id>', methods=['DELETE'])
def delete_emoji(id):
    """
    Delete a emoji
    :param id:
    :return:
    """
    try:
        emoji = Emoji.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    # remove Image for the deleted emoji
    try:
        imageDirectory = os.path.join(app.config.get('APP_ROOT'), 'static', 'uploads', 'emojis')
        os.remove(os.path.join(imageDirectory, emoji.imagefile))
    except OSError:
        pass

    emoji.delete()
    return build_response.sent_ok()