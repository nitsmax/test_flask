from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,IntField,\
    BooleanField, Document, DateTimeField,DecimalField,ReferenceField
import datetime
from app.countries.models import Country


class Voucher(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=200)
    code = StringField(max_length=50, required=True, unique=True)
    discount = DecimalField(default=0.00,precision=2,required=True,)
    uselimit = IntField(default=0)
    usedNum = IntField(default=0)
    membershipPlan = ListField(ReferenceField(Country))
    expireDate = DateTimeField()
    status = IntField(default=1)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)


    
