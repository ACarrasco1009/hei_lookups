from database import db

class SalesforceAccount(db.Model):
    __tablename__ = 'account'
    __table_args__ = {'schema': 'salesforce'}

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    facility_id = db.Column('facility_id__c', db.Integer)
    hei_2019_training_hours_completed = db.Column('hei_2019_training_hours_completed__c', db.String)
    state = db.Column('billingstate', db.String)
    city = db.Column('billingcity', db.String)
    hei_survey_target = db.Column('hei_survey_target__c', db.String)
    last_training_update = db.Column('HEI_Last_Training_Update__c', db.Date)
    record_type = db.Column('record_type_name__c', db.String)
    hei_2019_training_requirement = db.Column('hei_2019_training_requirement__c', db.String)
