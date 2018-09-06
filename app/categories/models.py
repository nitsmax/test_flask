from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,\
    BooleanField, Document, DateTimeField, ReferenceField, IntField
import datetime

class Category(Document):
    name = StringField(max_length=255, required=True, unique=True)
    imagefile = StringField(max_length=255)
    status = IntField()
    displayOrder = IntField()
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
