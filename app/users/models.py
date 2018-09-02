from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,\
    BooleanField, Document, DateTimeField,DecimalField,ReferenceField,IntField
import datetime


class MembershipPlan(Document):
    name = StringField(max_length=50, required=True, unique=True)
    description = StringField(max_length=200),
    amount = DecimalField(precision=2, required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
        
class User(Document):
    firstName = StringField(max_length=100, required=True)
    lastName = StringField(max_length=100)
    email = StringField(max_length=100)
    phoneNumber = StringField(max_length=12)
    password = StringField(max_length=255)
    imagefile = StringField(max_length=255)
    userType = StringField(required=True)
    countryCode = StringField(max_length=3, required=True)
    state = StringField(max_length=250, required=True)
    city = StringField(max_length=250)
    zipcode = StringField(max_length=20)
    membershipPlan = ReferenceField(MembershipPlan)
    memberShipExpDate = DateTimeField()
    status = IntField() # 1:Active, 2: Not varified, 3: Inactive, 4: Deleted
    signupType = IntField() # 1:Email, 2: Facebook, 3: Twitter, 4: Google, 5: Snapchat
    facebookId = StringField(max_length=100)
    twitterId = StringField(max_length=100)
    googleId = StringField(max_length=100)
    snapchatId = StringField(max_length=100)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)


    
