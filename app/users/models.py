from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,\
    BooleanField, Document, DateTimeField
import datetime


class User(Document):
    firstName = StringField(max_length=100, required=True)
    lastName = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True, unique=True)
    password = StringField(max_length=255)
    imagefile = StringField(max_length=255)
    userType = StringField(required=True)
    countryCode = StringField(max_length=3)
    state = StringField(max_length=250)
    city = StringField(max_length=250)
    zipcode = StringField(max_length=20)
    membershipPlan = ReferenceField(MembershipPlan)
    memberShipExpDate = DateTimeField()
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

    
