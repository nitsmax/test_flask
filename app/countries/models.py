from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,IntField,\
    BooleanField, Document, DateTimeField,DecimalField,ReferenceField
import datetime


class Country(Document):
    CountryName = StringField(max_length=100, required=True)
    CountryCode = StringField(max_length=5)
    countryCurrency = StringField(default='dollar')
    monthlyAmount = DecimalField(precision=2)
    displayOrder = IntField(default=1)
    Language = StringField(max_length=5)
    status = IntField(default=1)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
