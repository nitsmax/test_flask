import os
from flask import request, g, url_for
from flask import current_app as app
from app.emojis.models import Emoji, Category
from werkzeug.utils import secure_filename

def save_emoji(emoji):

    # check if the post request has the file part
    if 'Image' in request.files:
        imageDirectory = os.path.join(app.config.get('APP_ROOT'), 'static', 'uploads', 'emojis')
        # remove image file if it is update
        if emoji.imagefile is not None:
        	try:
        		os.remove(os.path.join(imageDirectory, emoji.imagefile))
        	except OSError:
        		pass
        	
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
        return {'emoji_id': str(emoji_id.id)}
    except Exception as e:
    	return {'error': str(e)}

def transpose_emoji(emoji):
	return {
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