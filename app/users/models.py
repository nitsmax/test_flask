from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,\
    BooleanField, Document, DateTimeField,DecimalField,ReferenceField,IntField
import datetime
from app.countries.models import Country

        
class User(Document):
    firstName = StringField(max_length=100, required=True)
    lastName = StringField(max_length=100)
    email = StringField(max_length=100)
    phoneNumber = StringField(max_length=12)
    password = StringField(max_length=255)
    imagefile = StringField(max_length=255)
    userType = StringField(required=True,default='User')
    countryCode = StringField(max_length=3, required=True)
    country = ReferenceField(Country)
    state = StringField(max_length=250, required=True)
    city = StringField(max_length=250)
    zipcode = StringField(max_length=20)
    membershipPlan = IntField(default=0) # 0:Free,1: Paid
    memberShipExpDate = DateTimeField()
    status = IntField(default=1) # 1:Active, 2: Not varified, 3: Inactive, 4: Deleted
    signupType = IntField() # 1:Email, 2: Facebook, 3: Twitter, 4: Google, 5: Snapchat
    facebookId = StringField(max_length=100)
    twitterId = StringField(max_length=100)
    googleId = StringField(max_length=100)
    snapchatId = StringField(max_length=100)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)


    
