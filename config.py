import os


class Config(object):
    DEBUG = False
    MONGODB_DB = "leloji"
    MONGODB_HOST = "127.0.0.1"
    MONGODB_PORT = 27017
    MONGODB_USERNAME = ""
    MONGODB_USERNAME = ""
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_ROOT = os.path.join(ROOT_DIR, 'app')

    # Intent Classifier model detials
    MODELS_DIR = "model_files/"
    INTENT_MODEL_NAME = "intent.model"
    DEFAULT_FALLBACK_INTENT_NAME = "fallback"
    DEFAULT_WELCOME_INTENT_NAME = "init_conversation"

    #File Upload Path
    UPLOAD_FOLDER = "uploads/"

    #Auth token
    KEY = 'secret'
    ACTIVATION_EXPIRE_DAYS = 5
    TOKEN_EXPIRE_HOURS = 1

    #braintree
    BT_ENVIRONMENT = 'sandbox'
    BT_MERCHANT_ID = 'hvk3qtwk5nydcz9d'
    BT_PUBLIC_KEY = '5qdpynz7j23dsn8j'
    BT_PRIVATE_KEY = 'bdee909188ba3dacc50a967c8d508931'


class Development(Config):
    DEBUG = True


class Production(Config):
    # MongoDB Database Details
    MONGODB_DB = "iky-ai"
    MONGODB_HOST = "mongodb"
    MONGODB_PORT = 27017
    MONGODB_USERNAME = ""
    MONGODB_USERNAME = ""

    # Web Server details
    WEB_SERVER_PORT = 8001
