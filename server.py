#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request
from twilio.jwt.access_token import AccessToken, VoiceGrant
from twilio.rest import Client
from datetime import date
import twilio.twiml
import urllib
import json
import urlparse

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SERVER = 'smtpout.secureserver.net'
EMAIL_USERNAME = 'voicemail@pd2g.com'
EMAIL_PASSWORD = 'VoicePPP@22'

ACCOUNT_SID = 'AC930ff2e97f313c236fe571db9987e5a0'
API_KEY = 'SKc0f6bc9d50890b39ee18a597bfd1f6a7'
API_KEY_SECRET = '5ALedwHKH9P2FzXSxCuwC4KZqp3MDvEb'
PUSH_CREDENTIAL_SID_IOS = 'CRe020cdf08fdc820e59a708458cda311e'

##CR46ae38c939adf11bee2ecdc8e9e4a0b1'

PUSH_CREDENTIAL_SID_ANDROID = 'CR0776cf10fe89986c7d40628e532dcd31'
APP_SID = 'APaafd4dcb530c4c3811e85738f4df3f7f'
AUTH_TOKEN = 'f2f4669503e0ca0b04a8ed3f50bb489b'
CONTACT_LIST = [{'userName': 'Phong'}, {'userName': 'Hiep'}]

IDENTITY = 'voice_test'
CALLER_ID = 'quick_start'

app = Flask(__name__)


@app.route('/accessToken', methods=['GET', 'POST'])
def token():
    client_name = request.values.get('client')
    platform = request.values.get('platform')
    account_sid = os.environ.get('ACCOUNT_SID', ACCOUNT_SID)
    api_key = os.environ.get('API_KEY', API_KEY)
    api_key_secret = os.environ.get('API_KEY_SECRET', API_KEY_SECRET)
    app_sid = os.environ.get('APP_SID', APP_SID)

    if platform == 'ios':
        push_credential_sid = os.environ.get('PUSH_CREDENTIAL_SID_IOS',
                PUSH_CREDENTIAL_SID_IOS)
    else:
        push_credential_sid = \
            os.environ.get('PUSH_CREDENTIAL_SID_ANDROID',
                           PUSH_CREDENTIAL_SID_ANDROID)

    if client_name:
        IDENTITY = client_name
        grant = VoiceGrant(push_credential_sid=push_credential_sid,
                           outgoing_application_sid=app_sid)

    token = AccessToken(account_sid, api_key, api_key_secret, IDENTITY)
    token.add_grant(grant)

    return str(token)


@app.route('/outbound', methods=['POST'])
def outbound():
    response = twiml.Response()
    with response.dial() as dial:
        dial.number('+16518675309')
    return str(response)


@app.route('/outgoing', methods=['GET', 'POST'])
def outgoing():
    resp = twilio.twiml.Response()
    from_value = request.values.get('From')
    caller = request.values.get('Caller')
    caller_value = caller[7:]
    to = request.values.get('To')
    if not (from_value and to):
        resp.say('Invalid request')
        return str(resp)
    from_client = caller.startswith('client')
    account_sid = os.environ.get('ACCOUNT_SID', ACCOUNT_SID)
    api_key = os.environ.get('API_KEY', API_KEY)
    api_key_secret = os.environ.get('API_KEY_SECRET', API_KEY_SECRET)
    client = Client(api_key, api_key_secret, account_sid)

    # caller_id = os.environ.get("CALLER_ID", CALLER_ID)

    if not from_client:

    # PSTN -> client
##?? fence off URL calls not from one URL

        print 'number:' + caller
        url = 'https://pdbook.herokuapp.com/getClient?phonenumber=' \
            + urllib.quote(to)
        response = urllib.urlopen(url)
        server_record = json.loads(response.read())
        if server_record:
            to_client = server_record['clientName']

#       ??is there a way to check the client status ?

        resp.dial(callerId=from_value,
                  action='https://pd2gvoice.herokuapp.com/call_completed'
                  ).client(to_client)
    elif to.startswith('client:'):

    # client -> client

        print 'client:' + caller

        resp.dial(callerId=caller_value,
                  action='https://pd2gvoice.herokuapp.com/call_completed'
                  ).client(to[7:])
    else:

    # client -> PSTN FriendlyName
    # ?? even cannot get caller ID we still need to deliver the call (by using a default caller)

        if caller.startswith('client'):
            print 'client:-> PSTN' + caller
            url = \
                'https://pdbook.herokuapp.com/getPhoneNumber?client_name=' \
                + caller[7:]
            response = urllib.urlopen(url)
            userCallerNumber = '+6531584308'
            server_record = json.loads(response.read())
            if server_record:
                userCallerNumber = server_record[0]['clientNum']

            resp.dial(callerId=userCallerNumber,
                      action='https://pd2gvoice.herokuapp.com/call_completed'
                      ).number(to)

            # except Exception, e:
            #    print e
            # finally:

            print 'client -> PSTN' + userCallerNumber

        # if call end or failed
        # resp.say("The call failed, or the remote party hung up. Goodbye.")

    return str(resp)


@app.route('/call_completed', methods=['GET', 'POST'])
def call_completed():
    resp = twilio.twiml.Response()
    from_value = request.values.get('From')
    caller = request.values.get('Caller')

    if request.values.get('DialCallStatus') == 'completed' \
        or request.values.get('DialCallStatus') == 'answered':
        resp.hangup()
    elif not caller.startswith('client'):
        resp.redirect('https://pd2gvoice.herokuapp.com/record_greeting')

            # "http://twimlets.com/menu?Message=Please%20press%20One%20for%20recording%20a%20voice%20mail%20&Options%5B1%5D=http%3A%2F%2Ftwimlets.com%2Fvoicemail%3FEmail%3Dinfo%2540powerdata2go.com%26Message%3Dplease%2520leave%2520your%2520message%2520%26Transcribe%3Dtrue%26&")

    return str(resp)


 # k = {'DialCallStatus': request.values.get("DialCallStatus")}

@app.route('/verification', methods=['GET', 'POST'])
def verification():
    account_sid = os.environ.get('ACCOUNT_SID', ACCOUNT_SID)
    api_key = os.environ.get('API_KEY', API_KEY)
    api_key_secret = os.environ.get('API_KEY_SECRET', API_KEY_SECRET)

    client = Client(api_key, api_key_secret, account_sid)
    try:
        phoneNumber = request.values.get('phoneNumber')
        friendlyName = request.values.get('friendlyName')
        new_phone = client.validation_requests.create(phoneNumber,
                friendly_name=friendlyName, call_delay=10)
        k = {'validation_code': str(new_phone.validation_code)}

        url = 'https://pdbook.herokuapp.com/addVerified?phonenumber=' \
            + urllib.quote(phoneNumber) + '&clientName=' + friendlyName

        response = urllib.urlopen(url)
        server_record = json.loads(response.read())
        if server_record:
            modified = server_record['nModified']
    except Exception, e:
        print 'error in call verification ' + phoneNumber + friendlyName
        print e
    finally:
        return json.dumps(k)


@app.route('/checkPhoneNumber', methods=['GET', 'POST'])
def checkPhoneNumber():
    account_sid = os.environ.get('ACCOUNT_SID', ACCOUNT_SID)
    api_key = os.environ.get('API_KEY', API_KEY)
    api_key_secret = os.environ.get('API_KEY_SECRET', API_KEY_SECRET)

    client = Client(api_key, api_key_secret, account_sid)

    phoneNumber = request.values.get('phoneNumber')
    caller_ids = \
        client.outgoing_caller_ids.list(phone_number=phoneNumber)
    k = {'verified': str(len(caller_ids) > 0),
         'phone_number': phoneNumber}
    return json.dumps(k)


@app.route('/callLog', methods=['GET', 'POST'])
def callLog():
    account_sid = os.environ.get('ACCOUNT_SID', ACCOUNT_SID)
    api_key = os.environ.get('API_KEY', API_KEY)
    api_key_secret = os.environ.get('API_KEY_SECRET', API_KEY_SECRET)

    client = Client(api_key, api_key_secret, account_sid)
    client_name = request.values.get('client')
    url = 'https://pdbook.herokuapp.com/getPhoneNumber?client_name=' \
        + client_name
    response = urllib.urlopen(url)
    userCallerNumber = '+6531584308'
    server_record = json.loads(response.read())
    if server_record:
        userCallerNumber = server_record[0]['clientNum']

    result = []
    for call in client.calls.list(to=userCallerNumber):
        if call.direction != 'inbound':
            tmp = {
                'contact': call.from_formatted,
                'type': 'Phone',
                'status': call.status,
                'duration': call.duration,
                'starttime': str(call.start_time),
                }
            result.append(tmp)
    for call in client.calls.list(from_=userCallerNumber,tarted_after=date(2017, 2, 2)):
        if call.direction != 'inbound':
            tmp = {
                'type': 'Outbox',
                'contact': call.to_formatted,
                'status': call.status,
                'duration': call.duration,
                'starttime': str(call.start_time),
                }
            result.append(tmp)
    k = {'Call': result}
    return json.dumps(k)


@app.route('/callMinutes', methods=['GET', 'POST'])
def callMinutes():
    account_sid = os.environ.get('ACCOUNT_SID', ACCOUNT_SID)
    api_key = os.environ.get('API_KEY', API_KEY)
    api_key_secret = os.environ.get('API_KEY_SECRET', API_KEY_SECRET)

    client = Client(api_key, api_key_secret, account_sid)
    client_name = request.values.get('client')

    url = 'https://pdbook.herokuapp.com/getPhoneNumber?client_name=' \
        + client_name
    response = urllib.urlopen(url)
    userCallerNumber = '+6531584308'
    server_record = json.loads(response.read())
    if server_record:
        userCallerNumber = server_record[0]['clientNum']

    result = 0
    for call in client.calls.list(to=userCallerNumber,
                                  status='completed',
                                  start_time=date.today()):
        if call.direction != 'inbound':
            result = result + int(call.duration)
    for call in client.calls.list(from_='client:' + client_name,
                                  status='completed',
                                  start_time=date.today()):
        if call.direction != 'inbound':
            result = result + int(call.duration)
    k = {'minutes': result}
    return json.dumps(k)


@app.route('/record_greeting', methods=['GET', 'POST'])
def index():
    resp = twilio.twiml.Response()
    resp.say('Hi, the user is not able to answer your call. This call is diverted to voicemail. Please leave your message after the tone.'
             )
    resp.record(maxLength='120', action='/record')
    return str(resp)


@app.route('/record', methods=['GET', 'POST'])
def handle_recording():
    recording_url = request.values.get('RecordingUrl', None)
    to_client = request.values.get('To', None)
    resp = twilio.twiml.Response()
    email_address = 'temp@pd2g.com'
    print 'to_client' + to_client

    if to_client is not None:
        url = 'https://pdbook.herokuapp.com/getEmail?phonenumber=' \
            + urllib.quote(to_client)
        response = urllib.urlopen(url)
        server_record = json.loads(response.read())
        if server_record:
            email_address = server_record['clientEmail']

    if recording_url is not None:
        resp.say('Thank you for your message.')
        recording_id = request.values.get('RecordingSid', None)
        caller_number = request.values.get('From', '(unknown)')
        from_address = 'PD2G Voicemail <voicemail@pd2g.com>'
        to_address = email_address
        parsed = urlparse.urlparse(recording_url)
        replaced_url = parsed._replace(netloc='voice.pd2g.com',
                scheme='http')

        email_subject = 'New voicemail from {0}'.format(caller_number)
        email_message = \
            """<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title> Voicemail </title></head><body>""" \
            + 'Dear User : A new voicemail has been received: {0}'.format(replaced_url.geturl())
        delete_message = \
            '<p> The voicemail is accessible to people with the URL. When you no longer need this voice mail, you can simply reply with keyword "Delete" and our system will delete this recording. <br> Thank you and Have a Great Day. '

        try:
            s = smtplib.SMTP(EMAIL_SERVER, 3535)
            s.login(EMAIL_USERNAME, EMAIL_PASSWORD)

            message = MIMEText(email_message + delete_message, 'html')
            message['Subject'] = email_subject
            message['From'] = from_address
            message['To'] = to_address
            bcc = ['info@powerdata2go.com']

# add bcc

            s.sendmail(from_address, [to_address] + bcc,
                       message.as_string())
        except Exception, e:

            print 'error in send VM email'
            print e
        finally:

            s.quit()
    else:

        resp.say('There was a problem with your voicemail.')
        resp.say('Goodbye.')

    return str(resp)


@app.route('/contactList', methods=['GET', 'POST'])
def contactList():
    return json.dumps({'contact': CONTACT_LIST})


@app.route('/', methods=['GET', 'POST'])
def welcome():
    resp = twilio.twiml.Response()
    resp.say('Welcome to Twilio')
    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
