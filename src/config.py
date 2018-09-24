import os
import base64

class Config:
    SQLALCHEMY_DATABASE_URI = base64.b64decode(os.environ['CIVIS_DB_URI']).decode()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_OPTIONS = {'ssl' : 'true',
                                   'sslfactory' : 'org.postgresql.ssl.NonValidatingFactory'}


