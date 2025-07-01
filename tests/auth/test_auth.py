from flask import session

def test_when_user_id_in_session_it_does_not_redirect(client):
    with client.session_transaction() as session:
        # set a user id without going through the login route
        session["user_id"] = 1

    response = client.get("/")
    assert response.status_code == 200

def test_when_user_id_not_in_session_it_redirects_to_mavis_sign_in(client):
    with client.session_transaction() as session:
        # set a user id without going through the login route
        session.pop("user_id", None)

    # session is saved now

    response = client.get("/", follow_redirects=False)
    # Check that the response had a redirect code.
    assert response.status_code == 302
    # Check what we were redirected to
    redirect_to = response.headers['Location'] 
    assert redirect_to.startswith( 'http://mavis-root.localhost/' )
    assert "/users/sign-in" in redirect_to;

    # TODO: Check that the return_url param on the redirect

 