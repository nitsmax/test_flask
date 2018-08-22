from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,\
    BooleanField, Document, DateTimeField, ReferenceField
import datetime
from app.users.models import User

class Category(Document):
    name = StringField(max_length=255, required=True, unique=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

class Emoji(Document):
    name = StringField(max_length=255, required=True)
    description = StringField(max_length=2000)
    tags = ListField(StringField(max_length=200))
    category = ReferenceField(Category)
    isPaid = BooleanField(required=True,default=True)
    imagefile = StringField(max_length=255)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)


class EmojiDownloads(Document):
    emoji = ReferenceField(Emoji)
    user = ReferenceField(User)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
