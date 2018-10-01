from flask import Flask, request, render_template
from database import db
from config import Config
import models
from sqlalchemy import and_

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def home():
    raw_token = request.args.get('civis_service_token') or ''
    token_parameter = f'?civis_service_token={raw_token}'
    return render_template('home.html', token_parameter=token_parameter)

@app.route("/training_hours", methods=['GET', 'POST'])
def training_hours_lookup():
    raw_token = request.args.get('civis_service_token')
    if len(request.args) == 1 and 'civis_service_token' in request.args:
        token_parameter = f'?civis_service_token={raw_token}'
    else:
        token_parameter = f'?{request.query_string.decode()}&civis_service_token={raw_token}'
    training_hours_completed = 0
    account_name = ''
    if request.method == 'POST':
        facility_id = request.form.get('facility_id') or ''
    else:
        facility_id = request.args.get('facility_id') or ''
    results = models.SalesforceAccount.query.filter(and_(models.SalesforceAccount.record_type == 'HEI',
                                                         models.SalesforceAccount.hei_survey_target != None,
                                                         models.SalesforceAccount.facility_id == facility_id
                                                         )).all()
    if len(results) > 1:
        template =  'training_hours/training_hours_error.html'
    elif not results:
        template = 'training_hours/training_hours_none.html'
    else:
        training_hours_completed = results[0].hei_2019_training_hours_completed or training_hours_completed
        account_name = results[0].name or ''
        template = 'training_hours/training_hours_completed.html'
    return render_template(template,
                           facility_id=facility_id,
                           training_hours_completed=training_hours_completed,
                           token_parameter=token_parameter,
                           account_name=account_name)

@app.route("/facility_id", methods=['GET', 'POST'])
def facility_id_lookup():
    raw_token = request.args.get('civis_service_token')
    if len(request.args) == 1 and 'civis_service_token' in request.args:
        token_parameter = f'?civis_service_token={raw_token}'
    else:
        token_parameter = f'?{request.query_string.decode()}&civis_service_token={raw_token}'
    if request.method == 'POST':
        org_name = request.form.get('org_name') or ''
        org_state = request.form.get('org_state') or ''
    else:
        org_name = request.args.get('org_name') or ''
        org_state = request.args.get('org_state') or ''
    if org_name != '':
        org_name = '%' + org_name + '%'
    results = models.SalesforceAccount.query.filter(and_(models.SalesforceAccount.record_type == 'HEI',
                                                         models.SalesforceAccount.facility_id is not None,
                                                         models.SalesforceAccount.facility_id != '',
                                                         models.SalesforceAccount.hei_survey_target != None,
                                                         models.SalesforceAccount.name.ilike(org_name.lower())))
    if org_state == '':
        results = results.all()
    else:
        results = results.filter(models.SalesforceAccount.state == org_state).all()
    results = sorted([(org.name or '', org.city or '', org.state or '', org.facility_id or '') for org in results], key=lambda org: (org[0], org[1], org[2], org[3]))
    return render_template('facility_id/facility_id.html', results=results, token_parameter=token_parameter)

if __name__ == '__main__':
    app.run(port=3838, threaded=True)
