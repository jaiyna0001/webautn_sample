from flask import Flask, render_template
from webauthn.webauthn import auth_app
import os
import json

settings = json.load(open('settings.json', 'r'))
app = Flask(__name__)
app.config['SERVER_NAME'] = settings["server_name"]
app.secret_key = os.urandom(32)

# GET /
@app.route('/')
def home():
  return '', 404


@app.route('/register')
def webauthn_register():
  return render_template('webauthn_register.html')


@app.route('/login')
def webauthn_login():
  return render_template('webauthn_login.html')


app.register_blueprint(auth_app)
app.run('0.0.0.0', port=443, ssl_context=('cert.crt', 'cert.key'))