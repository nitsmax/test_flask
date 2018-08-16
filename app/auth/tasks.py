import os
from flask import request, g, url_for
from flask import current_app as app
from app.users.models import User
from werkzeug.utils import secure_filename

def save_user(user):

    user.email = content.get("email")
    user.firstName = content.get("firstName")
    user.lastName = content.get("lastName")

    if content.get("password"):
        user.password = generate_password_hash(content.get("password"))

    if content.get("countryCode"):
        user.countryCode = content.get("countryCode")

    if content.get("state"):
        user.state = content.get("state")

    if content.get("city"):
        user.city = content.get("city")

    if content.get("zipcode"):
        user.zipcode = content.get("zipcode")

    user.userType = 'User'
    
    category = Category.objects(name=request.form.get("category")).get()
        if category:
            emoji.category = category
    user.membership = 'Free'
    
    try:
        user_id = user.save()
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
        'description': emoji.description,
        'image': '' if not emoji.imagefile else url_for('emojis_file', path=emoji.imagefile, _external=True),
        'date_created': emoji.date_created.isoformat(),
        'date_modified': emoji.date_modified.isoformat()
    }