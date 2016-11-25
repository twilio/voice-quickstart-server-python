import os
import json
from flask import Flask, request
from twilio.jwt.access_token import AccessToken, VoiceGrant
from twilio.rest import Client
from flask import url_for
import twilio.twiml

ACCOUNT_SID = 'AC64d6a7fa1eb934e5ed068f57e4ac16f9'
API_KEY = 'SK798c3d34afc34d650b1465606ccf640e'
API_KEY_SECRET = 'BM9ohnBeTGb3z9NJFGhsigG7TeDxhjCl'
PUSH_CREDENTIAL_SID_IOS = 'CR46ae38c939adf11bee2ecdc8e9e4a0b1'
PUSH_CREDENTIAL_SID_ANDROID = 'CR1d973685761d00a2d4cef10a88c2391d'
APP_SID = 'AP5dadf62e0240fad9dc927308b7dadc46'
AUTH_TOKEN = 'e1b308b76f84d974c871bb87719249bc'
CONTACT_LIST = [{'userName': 'Phong'}, {'userName': 'Dinh'}, {'userName': 'Antony'}, {'userName': 'Khanh'}, {'userName': 'Tan'}, {'userName': 'Hiep'}, {'userName': 'Thuc'}, {'userName': 'Tam'}, {'userName': 'Phi'}, {'userName': 'Jacob'}, {'userName': 'Stephanie'}, {'userName': 'Samita'}, {'userName': 'MoonShik'}, {'userName': 'Laurel'}, {'userName': 'Chelsea'}, {'userName': 'John'}, {'userName': 'Michael'}, {'userName': 'Andrew'}, {'userName': 'Kathryn'}, {'userName': 'Caleb'}, {'userName': 'Emily'}, {'userName': 'Isaac'}, {'userName': 'Hannah'}, {'userName': 'Barrett'}, {'userName': 'Elizabeth'}, {'userName': 'Dana'}, {'userName': 'Alisha'}, {'userName': 'Lewis'}, {'userName': 'Emma'}, {'userName': 'Quinn'}, {'userName': 'Benjamin'}, {'userName': 'Bianca'}, {'userName': 'Philip'}, {'userName': 'Kathryn'}, {'userName': 'Allison'}, {'userName': 'Jackson'}, {'userName': 'Oscar'}, {'userName': 'Corine'}, {'userName': 'Benjamin'}]

IDENTITY = 'voice_test'
CALLER_ID = 'quick_start'

app = Flask(__name__)

@app.route('/accessToken', methods=['GET', 'POST'])
def token():
  client_name = request.values.get('client')
  platform = request.values.get('platform')
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
  app_sid = os.environ.get("APP_SID", APP_SID)
  
  if platform == 'ios':
    push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID_IOS", PUSH_CREDENTIAL_SID_IOS)
  else:
    push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID_ANDROID", PUSH_CREDENTIAL_SID_ANDROID)
    
  if client_name:
     IDENTITY = client_name
  grant = VoiceGrant(
    push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )

  token = AccessToken(account_sid, api_key, api_key_secret, IDENTITY)
  token.add_grant(grant)

  return str(token)

@app.route('/incoming', methods=['GET', 'POST'])
def incoming():
  resp = twilio.twiml.Response()
  resp.say("Congratulations! You have received your first inbound call! Good bye.")
  return str(resp)

@app.route('/outbound', methods=['POST'])
def outbound():
    response = twiml.Response()
    with response.dial() as dial:
        dial.client(CALLER_ID)
    return str(response)
  
@app.route('/outgoing', methods=['GET', 'POST'])
def outgoing():
  IDENTITY = request.values.get('From')
  CALLER_ID = request.values.get('To')
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)

  client = Client(api_key, api_key_secret, account_sid)
  call = client.calls.create(to=CALLER_ID, from_=IDENTITY, url=url_for('.incoming', _external=True))
  return str(call.sid)

@app.route('/placeCall', methods=['GET', 'POST'])
def placeCall():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)

  client = Client(api_key, api_key_secret, account_sid)
  call = client.calls.create(url=request.url_root + 'incoming', to='client:' + 'hiep', from_='client:' + 'thuc')
  return str(call.sid)

@app.route('/callLog', methods=['GET', 'POST'])
def callLog():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)

  client = Client(api_key, api_key_secret, account_sid)
  client_name = request.values.get('client')
  result = []
  for call in client.calls.list(to="client:"+client_name):
    if call.direction != "inbound":
      tmp = {'from':call.from_formatted, 'to':call.to_formatted, 'status':call.status, 'duration':call.duration, 'starttime':str(call.start_time)}
      result.append(tmp)
  for call in client.calls.list(from_="client:"+client_name):
    if call.direction != "inbound":
      tmp = {'from':call.from_formatted, 'to':call.to_formatted, 'status':call.status, 'duration':call.duration, 'starttime':str(call.start_time)}
      result.append(tmp)
  k = {'Call': result}
  return json.dumps(k)

@app.route('/contactList', methods=['GET', 'POST'])
def contactList():
  return json.dumps({'contact': CONTACT_LIST})

@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
