from flask import Flask, render_template, request, redirect, url_for, session, flash
from cloudflare_api import CloudflareAPI
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session encryption

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        api_token = request.form.get('api_token')
        cf = CloudflareAPI(api_token)
        if cf.validate_token():
            session['api_token'] = api_token
            return redirect(url_for('search'))
        else:
            flash("Invalid API Token", "danger")
    return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'api_token' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        search_ip = request.form.get('search_ip')
        cf = CloudflareAPI(session['api_token'])
        records = cf.find_records_by_ip(search_ip)
        session['search_ip'] = search_ip
        session['records'] = records
        return render_template('results.html', records=records, search_ip=search_ip)
    return render_template('search.html')

@app.route('/update', methods=['POST'])
def update():
    if 'api_token' not in session:
        return redirect(url_for('login'))

    selected = request.form.getlist('selected')
    new_ip = request.form.get('new_ip')
    cf = CloudflareAPI(session['api_token'])

    results = []
    for rec_str in selected:
        zone_id, record_id = rec_str.split(',')
        result = cf.update_record_ip(zone_id, record_id, new_ip)
        results.append(result)

    flash("Updated {} records.".format(len(results)), "success")
    return redirect(url_for('search'))

if __name__ == '__main__':
    app.run(debug=True)