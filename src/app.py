from flask import Flask, request, render_template, url_for, redirect
from database import db
from config import Config
import models
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route("/training_hours", methods=['GET', 'POST'])
def training_hours_lookup():
    if request.method == 'POST':
        facility_id = request.form.get('facility_id') or ''
    else:
        facility_id = request.args.get('facility_id') or ''
    current_date = datetime.now().strftime('%B %d, %Y')
    all_found = models.SalesforceAccount.query.filter(models.SalesforceAccount.facility_id == facility_id).all()
    if len(all_found) > 1:
        template =  render_template('training_hours/training_hours_error.html', current_date=current_date)
    elif not all_found:
        template = render_template('training_hours/training_hours_none.html', current_date=current_date, facility_id=facility_id)
    else:
        training_hours_completed = all_found[0].hei_2019_training_hours_completed or 0
        template = render_template('training_hours/training_hours_completed.html', current_date=current_date, training_hours_completed=training_hours_completed)
    return template

@app.route("/facility_id", methods=['GET', 'POST'])
def facility_id_lookup():
    if request.method == 'POST':
        org_name = '%' + request.form.get('org_name') + '%'or ''
        org_state = request.form.get('org_state')
    else:
        org_name = '%' + request.args.get('org_name') + '%' or ''
        org_state = request.args.get('org_state')
    current_date = datetime.now().strftime('%B %d, %Y')
    results = models.SalesforceAccount.query.filter(models.SalesforceAccount.facility_id is not None).filter(models.SalesforceAccount.facility_id != '')
    results = results.filter(models.SalesforceAccount.name.ilike(org_name.lower()))
    if org_state == '':
        results = results.all()
    else:
        results = results.filter(models.SalesforceAccount.state == org_state).all()
    results = sorted([(org.name or '', org.state or '', org.facility_id or '') for org in results], key=lambda org: (org[0], org[1], org[2]))
    return render_template('facility_id/facility_id.html', results=results, current_date=current_date)

if __name__ == '__main__':
    app.run(port=3838)
