from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,\
    BooleanField, Document, DateTimeField, ReferenceField
import datetime


class LabeledSentences(EmbeddedDocument):
    id = ObjectIdField(required=True, default=lambda: ObjectId())
    data = ListField(required=True)


class Parameter(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId())
    name = StringField(required=True)
    required = BooleanField(default=False)
    type = StringField(required=False)
    prompt = StringField()


class ApiDetails(EmbeddedDocument):
    url = StringField(required=True)
    requestType = StringField(
        choices=[
            "POST",
            "GET",
            "DELETE",
            "PUT"],
        required=True)
    headers = ListField(default=[])
    isJson = BooleanField(default=False)
    jsonData = StringField(default="{}")

    def get_headers(self):
        headers = {}
        for header in self.headers:
            headers[header["headerKey"]]=header["headerValue"]
        return headers

class Category(Document):
    name = StringField(max_length=255, required=True, unique=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

class Emoji(Document):
    name = StringField(max_length=255, required=True)
    description = StringField(max_length=2000)
    tags = ListField(StringField(max_length=200))
    category = ReferenceField(Category)
    isPaid = BooleanField(required=True,default=True)
    imagefile = StringField(max_length=255)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
