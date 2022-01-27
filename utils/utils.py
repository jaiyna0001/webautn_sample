from base64 import b64encode, b64decode
from fido2 import cbor
from fido2.ctap2 import AttestedCredentialData
from flask import Response
from random import SystemRandom

import json
import string

class Utils():
  @classmethod
  def create_response(self, data: dict):
    return Response(Utils.encode_data(data), mimetype='text/plain')

  @classmethod
  def result_ok(self):
    return Utils.create_response({'status': 'OK'})

  @classmethod
  def result_ng(self):
    return Utils.create_response({'status': 'NG'})

  @classmethod
  def encode_data(self, data: dict):
    return b64encode(cbor.encode(data)).decode('utf-8')

  @classmethod
  def decode_data(self, data):
    return cbor.decode(b64decode(data))

  @classmethod
  def random_string(self, length=32):
    return ''.join([SystemRandom().choice(string.ascii_letters + string.digits) for i in range(length)])

  @classmethod
  def random_bytes(self, length=32):
    return bytes(Utils.random_string(length), 'utf-8')

  @classmethod
  def get_users(self, path):
    with open('{}/data/users.json'.format(path), encoding='utf-8') as f:
      users = json.load(f)
    return users

  @classmethod
  def append_user(self, path, user_name, credential):
    users = Utils.get_users(path)
    with open('{}/data/users.json'.format(path), mode='wt', encoding='utf-8') as f:
      users[user_name] = {
        'display_name': user_name,
        'credential': Utils.encode_data(credential.__dict__)
      } 
      json.dump(users, f, ensure_ascii=False, indent=2)

  @classmethod
  def get_credentials(self, path, user_name):
    users = Utils.get_users(path)
    user = users.get(user_name)
    if user != None:
      return [AttestedCredentialData.create(**Utils.decode_data(user['credential']))]
    else:
      return []

  @classmethod
  def get_display_name(self, path, user_name):
    users = Utils.get_users(path)
    user = users.get(user_name)
    if user != None:
      return user['display_name']
    else:
      return None