from datetime import datetime, timezone
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

import dateutil.parser
import json
import logging
import requests
import urllib.parse, urllib.request 

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)

def session_expired():
    last_visit = session.get('last_visit')
    if last_visit is None:
        return True
    
    session_age = (datetime.now().astimezone(timezone.utc) - last_visit).total_seconds()
    return abs(session_age) > current_app.config['SESSION_TTL_SECONDS']
    
def is_logged_in():
    if 'user_id' in session:
        if session_expired():
            session.clear()
            return False
        else:
            return True
        
    else:
        return False

def mavis_url(path):
    return current_app.config['MAVIS_ROOT_URL'] + path

def verify_token(token):
    url = mavis_url('/tokens/' + token)
    user_data = None

    headers = {'Authorization' :current_app.config['SECRET_KEY']}
    r = requests.get(url, headers=headers)
    logger.info('response from verify_token call', r.status_code)
    logger.info('response body ', r.text)

    user_data = r.json()

    return user_data

def log_user_in(data):
    session['user_id'] = data['user_id']
    session['created_at'] = data['created_at']
    session['last_visit'] = datetime.now()
    session['cis2_info'] = data['cis2_info']
    session['user'] = data['user']

@main.route("/")
def index():
    if not is_logged_in():
        token = request.args.get('token')
        if token:
            # TODO: If we're given a token, verify it
            user_data = verify_token(token)
            log_user_in(user_data)
        else:
            target_url = mavis_url('/start?redirect_after_login=' + urllib.parse.quote(request.url))
            return redirect(target_url)
        
    return render_template("index.jinja")
