import os
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g
from flask import current_app as app
from app.commons import build_response
from app.categories.models import Category
from app.auth.models import login_required
from app.categories.tasks import save_category, transpose_category


categories = Blueprint('categories_blueprint', __name__,
                    url_prefix='/api/categories')

@categories.route('', methods=['POST'])
def create_category():
    """
    Create a story from the provided json
    :param json:
    :return:
    """
    category = Category()
    try:
        save_response = save_category(category)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({
                "_id": str(save_response['category_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})

@categories.route('')
#@login_required
def read_categories():
    """
    find list of categories for the agent
    :return:
    """
    categories = Category.objects().order_by('name')
    if not categories:
        return build_response.build_json([])

    response_categories = []

    for category in categories:
        obj_category = transpose_category(category)
        response_categories.append(obj_category)
    return build_response.build_json(response_categories)

@categories.route('/findcategories')
def find_categories():
    """
    find list of categories for the agent
    :return:
    """
    categories = Category.objects(status=1).order_by('name')
    if not categories:
        return build_response.build_json([])

    response_categories = []

    for category in categories:
        obj_category = transpose_category(category)
        response_categories.append(obj_category)
    return build_response.build_json(response_categories)

@categories.route('/<id>')
def read_category(id):
    """
    Find details for the given category id
    :param id:
    :return:
    """
    try:
        category = Category.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    return build_response.build_json(transpose_category(category))


@categories.route('/<id>', methods=['PUT'])
def update_category(id):
    category = Category.objects.get(id=ObjectId(id))
    try:
        save_response = save_category(category)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({
                "_id": str(save_response['category_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})



@categories.route('/<id>', methods=['DELETE'])
def delete_category(id):
    """
    Delete a category
    :param id:
    :return:
    """
    try:
        category = Category.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    # remove Image for the deleted category
    try:
        if category.imagefile:
            imageDirectory = os.path.join(app.config.get('APP_ROOT'), 'static', 'uploads', 'categories')
            os.remove(os.path.join(imageDirectory, category.imagefile))
            
    except OSError:
        pass

    category.delete()
    return build_response.sent_ok()

@categories.route('/user-category-download', methods=['POST'])
def user_category_download():
    """
    user download a category
    """
    try:
        save_response = category_download()
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({
                "_id": str(save_response['category_download_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})