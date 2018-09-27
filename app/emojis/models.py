from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,\
    BooleanField, Document, DateTimeField, ReferenceField
import datetime
from app.users.models import User
from app.categories.models import Category
from app.countries.models import Country

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
    country = ReferenceField(Country)
    region = StringField()
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
