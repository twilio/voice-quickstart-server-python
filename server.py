import os
import json
from flask import Flask, request
from twilio.jwt.access_token import AccessToken, VoiceGrant
from twilio.rest import Client
from datetime import date
import twilio.twiml

ACCOUNT_SID = 'AC930ff2e97f313c236fe571db9987e5a0'
API_KEY = 'SKc0f6bc9d50890b39ee18a597bfd1f6a7'
API_KEY_SECRET = '5ALedwHKH9P2FzXSxCuwC4KZqp3MDvEb'
PUSH_CREDENTIAL_SID_IOS = 'CRe020cdf08fdc820e59a708458cda311e' 
##CR46ae38c939adf11bee2ecdc8e9e4a0b1'

PUSH_CREDENTIAL_SID_ANDROID = 'CR0776cf10fe89986c7d40628e532dcd31'
APP_SID = 'APaafd4dcb530c4c3811e85738f4df3f7f'
AUTH_TOKEN = 'f2f4669503e0ca0b04a8ed3f50bb489b'
CONTACT_LIST = [{'userName': 'Phong'}, {'userName': 'Dinh'}, {'userName': 'Antony'}, {'userName': 'Khanh'}, {'userName': 'Tan'}, {'userName': 'Hiep'}]

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
     IDENTITY =client_name
  grant = VoiceGrant(
    push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )

  token = AccessToken(account_sid, api_key, api_key_secret, IDENTITY)
  token.add_grant(grant)

  return str(token)

@app.route('/outbound', methods=['POST'])
def outbound():
    response = twiml.Response()
    with response.dial() as dial:
        dial.number("+16518675309")
    return str(response)
  
@app.route('/outgoing', methods=['GET', 'POST'])
def outgoing():
  resp = twilio.twiml.Response()
  from_value = request.values.get('From')
  caller = request.values.get('Caller')
  caller_value=caller[7:]
  to = request.values.get('To')
  if not (from_value and to):
    resp.say("Invalid request")
    return str(resp)
  from_client = caller.startswith('client')
  # caller_id = os.environ.get("CALLER_ID", CALLER_ID)
  if not from_client:
    # PSTN -> client
    if to.startswith('+653158426'):
        to_client = 'ClientDavid'
    elif to.startswith('+8525803668'):
        to_client = 'antony_hkg'
    elif to.startswith('+653158430'):
        to_client = 'BKK-TEST'
    elif to.startswith('+653158424'):
        to_client = 'testing_SG'
    else:
        to_client = 'failed_no_client_map'
    
    resp.dial(callerId=from_value).client(to_client)
  elif to.startswith("client:"):
    # client -> client
    resp.dial(callerId=caller_value).client(to[7:])
  else:
    # client -> PSTN
    if caller.startswith('client:antony_tes'):
        caller_value = '+6584976337'
    if caller.startswith('client:ClientDavi'):
        caller_value = '+6590175007'
    if caller.startswith('client:antony_hk'):
        caller_value = '+85258036680'
    if caller.startswith('client:testing_SG'):
        caller_value = '+6531584242'
    if caller.startswith('client:BKK-TE'):
        caller_value = '+6531584308'
    resp.dial(callerId=caller_value).number(to)

  # if call end or failed
  # resp.say("The call failed, or the remote party hung up. Goodbye.")
  return str(resp)

@app.route('/verification', methods=['GET', 'POST'])
def verification():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)		
  		  
  client = Client(api_key, api_key_secret, account_sid)
  
  phoneNumber = request.values.get('phoneNumber')
  friendlyName = request.values.get('friendlyName')
  new_phone = client.validation_requests.create(phoneNumber, friendly_name=friendlyName, call_delay=30)
  return str(new_phone.validation_code)

@app.route('/checkPhoneNumber', methods=['GET', 'POST'])
def checkPhoneNumber():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)		
  		  
  client = Client(api_key, api_key_secret, account_sid)
  
  phoneNumber = request.values.get('phoneNumber')
  caller_ids = client.outgoing_caller_ids.list(phone_number=phoneNumber)
  return len(caller_ids) > 0

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
      tmp = {'contact':call.from_formatted, 'type':'Inbox', 'status':call.status, 'duration':call.duration, 'starttime':str(call.start_time)}
      result.append(tmp)
  for call in client.calls.list(from_="client:"+client_name):
    if call.direction != "inbound":
      tmp = {'type':'Outbox', 'contact':call.to_formatted, 'status':call.status, 'duration':call.duration, 'starttime':str(call.start_time)}
      result.append(tmp)
  k = {'Call': result}
  return json.dumps(k)

@app.route('/callMinutes', methods=['GET', 'POST'])
def callMinutes():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)		
  		  
  client = Client(api_key, api_key_secret, account_sid)
  client_name = request.values.get('client')
  result = 0
  for call in client.calls.list(to="client:"+client_name, status="completed", start_time=date.today()):
    if call.direction != "inbound":
      result = result + int(call.duration)
  for call in client.calls.list(from_="client:"+client_name, status="completed", start_time=date.today()):
    if call.direction != "inbound":
      result = result + int(call.duration)
  k = {'minutes': result}
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
