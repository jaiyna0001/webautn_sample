from __future__ import print_function, absolute_import, unicode_literals

from fido2.webauthn import PublicKeyCredentialRpEntity
from fido2.client import ClientData
from fido2.server import Fido2Server
from fido2.ctap2 import AttestationObject, AuthenticatorData, AttestedCredentialData
from flask import Blueprint, session, request
from utils.utils import Utils

import json
import os

settings = json.load(open('settings.json', 'r'))
path = os.path.splitext(os.path.basename(__file__))[0]
auth_app = Blueprint(path, __name__, url_prefix='/{}'.format(path))
rp = PublicKeyCredentialRpEntity(settings['server_name'], 'Demo server')
server = Fido2Server(rp)
credentials = []


@auth_app.route('/')
def index():
  return Utils.result_ng()


@auth_app.route('/register/begin', methods=['POST'])
def register_begin():
  data = Utils.decode_data(request.get_data())
  user_name = data['name']
  credentials = Utils.get_credentials(path, user_name)
  if credentials != []:
    print('already regist user: {}.'.format(user_name))
    return Utils.result_ok()
  registration_data, state = server.register_begin(
    {
      'id': Utils.random_bytes(),
      'name': user_name,
      'displayName': user_name,
    },
    credentials,
    user_verification='required',
    authenticator_attachment='platform',
  )

  registration_data['status'] = 'OK'
  session['state'] = state
  session['user_name'] = user_name
  return Utils.create_response(registration_data)


@auth_app.route('/register/complete', methods=['POST'])
def register_complete():
  user_name = session['user_name']
  data = Utils.decode_data(request.get_data())
  client_data = ClientData(data['clientDataJSON'])
  att_obj = AttestationObject(data['attestationObject'])

  auth_data = server.register_complete(session['state'], client_data, att_obj)

  Utils.append_user(path, user_name, auth_data.credential_data)
  session.pop('user_name')
  return Utils.result_ok()


@auth_app.route('/authenticate/begin', methods=['POST'])
def authenticate_begin():
  data = Utils.decode_data(request.get_data())
  user_name = data['name']
  credentials = Utils.get_credentials(path, user_name)
  if not credentials:
    print('not exists credential.')
    return Utils.result_ng()

  auth_data, state = server.authenticate_begin(credentials)
  auth_data['status'] = 'OK'
  session['state'] = state
  session['user_name'] = user_name
  return Utils.create_response(auth_data)


@auth_app.route('/authenticate/complete', methods=['POST'])
def authenticate_complete():
  user_name = session['user_name']
  credentials = Utils.get_credentials(path, user_name)
  if not credentials:
    print('not exists credential.')
    return Utils.result_ng()

  data = Utils.decode_data(request.get_data())
  credential_id = data['credentialRawId']
  client_data = ClientData(data['clientDataJSON'])
  auth_data = AuthenticatorData(data['authenticatorData'])
  signature = data['signature']

  server.authenticate_complete(
    session.pop('state'),
    credentials,
    credential_id,
    client_data,
    auth_data,
    signature,
  )
  result = {
    'status': 'OK',
    'display_name': Utils.get_display_name(path, user_name)
  }
  session.pop('user_name')
  return Utils.create_response(result)