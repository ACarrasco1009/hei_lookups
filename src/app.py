from flask import Flask, request, render_template, make_response
from database import db
from config import Config
import models
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def home():
    raw_token = request.args.get('civis_service_token') or ''
    token_parameter = f'?civis_service_token={raw_token}'
    resp = make_response(render_template('home.html', token_parameter=token_parameter))
    resp.set_cookie('civis_service_token', raw_token)
    return resp

@app.route("/training_hours", methods=['GET', 'POST'])
def training_hours_lookup():
    raw_token = request.args.get('civis_service_token') or request.cookies.get('civis_service_token')
    if len(request.args) == 1 and 'civis_service_token' in request.args:
        token_parameter = f'?civis_service_token={raw_token}'
    else:
        token_parameter = f'?{request.query_string.decode()}&civis_service_token={raw_token}'
    training_hours_completed = 0
    current_date = datetime.now().strftime('%B %d, %Y')
    if request.method == 'POST':
        facility_id = request.form.get('facility_id') or ''
    else:
        facility_id = request.args.get('facility_id') or ''
    all_found = models.SalesforceAccount.query.filter(models.SalesforceAccount.facility_id == facility_id).all()
    if len(all_found) > 1:
        template =  'training_hours/training_hours_error.html'
    elif not all_found:
        template = 'training_hours/training_hours_none.html'
    else:
        training_hours_completed = all_found[0].hei_2019_training_hours_completed or training_hours_completed
        template = 'training_hours/training_hours_completed.html'
    return render_template(template,
                           current_date=current_date,
                           facility_id=facility_id,
                           training_hours_completed=training_hours_completed,
                           token_parameter=token_parameter)

@app.route("/facility_id", methods=['GET', 'POST'])
def facility_id_lookup():
    raw_token = request.args.get('civis_service_token') or request.cookies.get('civis_service_token')
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
    current_date = datetime.now().strftime('%B %d, %Y')
    results = models.SalesforceAccount.query.filter(models.SalesforceAccount.facility_id is not None).filter(models.SalesforceAccount.facility_id != '')
    results = results.filter(models.SalesforceAccount.name.ilike(org_name.lower()))
    if org_state == '':
        results = results.all()
    else:
        results = results.filter(models.SalesforceAccount.state == org_state).all()
    results = sorted([(org.name or '', org.state or '', org.facility_id or '') for org in results], key=lambda org: (org[0], org[1], org[2]))
    return render_template('facility_id/facility_id.html', results=results, current_date=current_date, token_parameter=token_parameter)

if __name__ == '__main__':
    app.run(port=3838)
