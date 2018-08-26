from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,IntField,\
    BooleanField, Document, DateTimeField,DecimalField,ReferenceField
import datetime
from app.users.models import MembershipPlan


class Voucher(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=200)
    code = StringField(max_length=50, required=True, unique=True)
    uselimit = IntField()
    usedNum = IntField()
    membershipPlan = ReferenceField(MembershipPlan)
    expireDate = DateTimeField()
    status = IntField()
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)


    
