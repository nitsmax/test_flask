from flask import current_app as app
from app.users.models import User
from app.commons import build_response
from flask import request, g
import functools
import jwt


from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,IntField,\
    BooleanField, Document, DateTimeField,DecimalField,ReferenceField
import datetime
from app.users.models import User
from app.countries.models import Country
from app.vouchers.models import Voucher


class Subscription(Document):
    user = ReferenceField(User)
    membershipPlan = ReferenceField(Country)
    paymentGateway = StringField()
    paymentMethod = StringField()
    membershipAmount = DecimalField(precision=2)
    paymentAmount = DecimalField(precision=2)
    currency = StringField()
    voucher = ReferenceField(Voucher)
    paymentInfo = StringField()
    subscriptionId = StringField()
    subscriptionPlan = StringField()
    subscriptionInfo = StringField()
    subscriptionStatus = StringField(default='Initial')
    subscriptionCancelDate = DateTimeField()
    subscriptionNextBillingDate = DateTimeField()
    failedMessage = StringField()
    failedCode = StringField()
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

class Transaction(Document):
    user = ReferenceField(User)
    subscription = ReferenceField(Subscription)
    paymentGateway = StringField()
    paymentMethod = StringField()
    amount = DecimalField(precision=2)
    currency =  StringField()
    paymentInfo = StringField()
    subscriptionId = StringField()
    paymentStatus = StringField()
    failedMessage = StringField(default=1)
    failedCode = StringField(default=1)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
