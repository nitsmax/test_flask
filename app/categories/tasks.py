import os
from flask import request, g, url_for
from flask import current_app as app
from app.categories.models import Category
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

def save_category(category):

    # check if the post request has the file part
    if 'Image' in request.files:
        imageDirectory = os.path.join(app.config.get('APP_ROOT'), 'static', 'uploads', 'categories')
        # remove image file if it is update
        if category.imagefile is not None:
            try:
                os.remove(os.path.join(imageDirectory, category.imagefile))
            except OSError:
                pass
            
        file = request.files['Image']

        filename = secure_filename(file.filename)
        file.save(os.path.join(imageDirectory, filename))
        category.imagefile = filename

    category.name = request.form['name']
    category.status = 2 if request.form['status'] == 'Inactive' else 1

    try:
        category_id = category.save()
        return {'category_id': str(category_id.id)}
    except Exception as e:
        return {'error': str(e)}

def transpose_category(category):
    return {
        '_id': str(category.id),
        'name': category.name,
        'status' : 'Inactive' if category.status == 2 else 'Active',
        'image': '' if not category.imagefile else url_for('categories_file', path=category.imagefile, _external=True),
        'date_created': category.date_created.isoformat(),
        'date_modified': category.date_modified.isoformat()
    }