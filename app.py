from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import json
import mysql.connector

import os 
import requests
from oauthlib.oauth2 import WebApplicationClient
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_PATH'] = '/'
cors = CORS(app)
app.secret_key = os.urandom(24) # add the secret key here
bcrypt = Bcrypt(app)
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='my-mysql-password',
    database='web'
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)


    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (users_email,))
    result = cursor.fetchall()
    if not result:
        print("no need to commit")
        cursor.execute("INSERT INTO users (username, payment, sub_id) VALUES (%s, %s, %s)", (users_email, "false", ""))
        db.commit()
    session["email"] = users_email

    return redirect("/")




@app.route('/logout', methods=['POST'])
def logout():
    # Remove the user's email from the session
    session.clear()
    return redirect("/")


@app.route("/secret", methods=["GET"])
def secret():
    if not session.get("email"):
        return redirect("/")
    elif session.get("email") and check_payment_status(session["email"]) is False:
        return render_template("payment.html")
    return render_template('secret.html')

kubectl -n kube-system get cm anodot-forecast.v1276 -o jsonpath="{.data.release}" | \
base64 -d | gunzip | \
hprotoc --decode hapi.release.Release  $(find ~/remove/helm/_proto/hapi -name "*.proto"  -exec echo -n "{} " \;)\
> ~/Work/forecast_fix/anodot-forecast.v127.txt



kubectl -n kube-system get cm anodot-forecast.v126 -o jsonpath="{.data.release}" | \
base64 -d | gunzip | \
hprotoc --decode hapi.release.Release  $(find ~/remove/helm/_proto/hapi -name "*.proto"  -exec echo -n "{} " \;)\
> ~/Work/forecast_fix/anodot-forecast.v126.txt
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

def check_payment_status(username):

    # Create a cursor object to execute queries
    cursor = db.cursor()

    # Execute the query to get the payment value for the given username
    query = f"SELECT payment FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()
    # Check the value of the payment column for the given username
    if result and result[0][0] == "false":
        return False
    else:
        return True
@app.route("/payment", methods=["GET"])
def payment_gateway():
    user = session["email"]
    if not user :
        return redirect("/")
    elif user and check_payment_status(user) is False:
        return render_template("payment.html")
    return redirect("/secret")






@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html")

@app.route("/success", methods=["POST"])
def redirect_to_success():
    return render_template("secret.html")

@app.route("/cancel")
def cancelled():
    return render_template("cancel.html")


if __name__ == "__main__":
    app.run(debug=True,ssl_context="adhoc")
