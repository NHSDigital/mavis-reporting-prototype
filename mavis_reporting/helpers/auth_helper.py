from datetime import datetime, timedelta, timezone

from mavis_reporting.helpers import mavis_helper

def session_expired(session, current_app):
    last_visit = session.get('last_visit')
    if last_visit is None:
        return True
    
    session_age = (datetime.now().astimezone(timezone.utc) - last_visit).total_seconds()
    return abs(session_age) > current_app.config['SESSION_TTL_SECONDS']
    
def is_logged_in(session, current_app):
    if 'user_id' in session:
        if session_expired(session, current_app):
            session.clear()
            return False
        else:
            return True
        
    else:
        return False

def log_user_in(data, session):
    session['user_id'] = data['user_id']
    session['created_at'] = data['created_at']
    session['last_visit'] = datetime.now()
    session['cis2_info'] = data['cis2_info']
    session['user'] = data['user']
    