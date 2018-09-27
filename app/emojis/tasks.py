import os
from flask import request, g, url_for
from flask import current_app as app
from app.emojis.models import Emoji, EmojiDownloads
from app.categories.models import Category
from app.users.models import User
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

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

    if request.form['isPaid'] == 'Paid':
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
        '_id': str(emoji.id),
        'name': emoji.name,
        'isPaid': 'Paid' if emoji.isPaid == True else 'Free',
        'isPaidB': emoji.isPaid,
        'tags': emoji.tags,
        'category' : emoji.category.name if emoji.category else '',
        'description': emoji.description if emoji.description else '',
        'image': '' if not emoji.imagefile else url_for('emojis_file', path=emoji.imagefile, _external=True),
        'date_created': emoji.date_created.isoformat(),
        'date_modified': emoji.date_modified.isoformat()
    }

def emoji_download(emoji_id, user):
    try:
        emoji = Emoji.objects.get(id=ObjectId(emoji_id))
        print("emoji",emoji)
        if not emoji:
            raise Exception("No Emoji Found")

        emojiDownloads = EmojiDownloads()
        emojiDownloads.user = user
        emojiDownloads.emoji = emoji
        emojiDownloads.country = user.country
        emojiDownloads.region = user.state

        emoji_download_id = emojiDownloads.save()
        return {'emoji_download_id': str(emoji_download_id.id)}
    except Exception as e:
        print(str(e))
        return {'error': str(e)}