from database import db

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'ID: {self.id}, Name: {self.name}'


class MobileCommonsProfile(db.Model):
    __tablename__ = 'profiles'
    __table_args__ = {'schema': 'mobile_commons'}

    profile_id = db.Column('profile_id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String)
    last_name = db.Column('last_name', db.String)
    phone_number = db.Column('phone_number', db.String)
    email = db.Column('email', db.String)
    status = db.Column('status', db.String)
    source_type = db.Column('source_type', db.String)
    created_at = db.Column('created_at', db.DateTime)
    updated_at = db.Column('updated_at', db.DateTime)
    opted_out_at = db.Column('opted_out_at', db.DateTime)
    outed_out_source = db.Column('outed_out_source', db.String)
    source_name = db.Column('source_name', db.String)
    address_street1 = db.Column('address_street1', db.String)
    address_street2 = db.Column('address_street2', db.String)
    address_city = db.Column('address_city', db.String)
    address_state = db.Column('address_state', db.String)
    address_postal_code = db.Column('address_postal_code', db.String)
    address_country = db.Column('address_country', db.String)
    location_latitude = db.Column('location_latitude', db.Float)
    location_longitude = db.Column('location_longitude', db.Float)
    run_date = db.Column('run_date', db.DateTime)

class SalesforceAccount(db.Model):
    __tablename__ = 'account'
    __table_args__ = {'schema': 'salesforce'}

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    facility_id = db.Column('facility_id__c', db.Integer)
    hei_2019_training_hours_completed = db.Column('hei_2019_training_hours_completed__c', db.Integer)
    state = db.Column('billingstate', db.String)
    city = db.Column('billingcity', db.String)
    hei_survey_target = db.Column('hei_survey_target__c', db.String)
    last_training_update = db.Column('HEI_Last_Training_Update__c', db.Date)
    record_type = db.Column('record_type_name__c', db.String)