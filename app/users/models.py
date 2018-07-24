from bson.objectid import ObjectId
from mongoengine.fields import ListField,\
    EmbeddedDocumentListField, EmbeddedDocumentField, EmbeddedDocument,\
    ObjectIdField, StringField,\
    BooleanField, Document, DateTimeField
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

class User(Document):
    firstName = StringField(max_length=100, required=True)
    lastName = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True, unique=True)
    password = StringField(max_length=255, required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
