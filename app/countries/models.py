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

class Countries(Document):
    Name = StringField(max_length=100, required=True)
    Code = StringField(max_length=5)

class States(Document):
    countryCode = StringField(max_length=5, required=True)
    stateCode = StringField(max_length=5, required=True)
    stateName = StringField(max_length=100, required=True)
    stateType = StringField(max_length=20, required=True)
        