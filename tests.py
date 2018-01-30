import jwt
import os
import requests
import unittest

"""
Integration tests for validating the server quickstart routes

Set environment variable VOICE_SERVER_URL to the server url to run the tests

Running tests with nose:
> export VOICE_SERVER_URL=http://localhost:5000; nosetests

"""
class TestRoutes(unittest.TestCase):
    DEFAULT_CALLER_ID = "client:quick_start"
    DEFAULT_NUMBER_CALLER_ID = "1234567890"
    DEFAULT_IDENTITY = "alice"
    DEFAULT_MESSAGE = "Welcome to Twilio"
    ALTERNATE_IDENTITY = "bob"
    PHONE_NUMBER = "12345" 

    def setUp(self):
        self.voice_server_url = os.environ.get("VOICE_SERVER_URL")
        self.assertTrue(
                self.voice_server_url,
                "Set environment variable VOICE_SERVER_URL to run the test")

    def test_get_root(self):
        r = requests.get(self.voice_server_url)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue(self.DEFAULT_MESSAGE in r.text)

    def test_post_root(self):
        r = requests.post(self.voice_server_url)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue(self.DEFAULT_MESSAGE in r.text)

    def test_get_access_token(self):
        r = requests.get(self.voice_server_url + "/accessToken")
        self.assertEquals(requests.codes.ok, r.status_code)
        access_token = jwt.decode(r.text, verify=False)
        self.validate_access_token(access_token, self.DEFAULT_IDENTITY)

    def test_post_access_token(self):
        r = requests.post(self.voice_server_url + "/accessToken")
        self.assertEquals(requests.codes.ok, r.status_code)
        access_token = jwt.decode(r.text, verify=False)
        self.validate_access_token(access_token, self.DEFAULT_IDENTITY)

    def test_get_access_token_with_identity(self):
        identity = self.ALTERNATE_IDENTITY 
        payload = {'identity': identity }
        r = requests.get(self.voice_server_url + "/accessToken", params=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        access_token = jwt.decode(r.text, verify=False)
        self.validate_access_token(access_token, identity)

    def test_post_access_token_with_identity(self):
        identity = self.ALTERNATE_IDENTITY 
        payload = {'identity': identity }
        r = requests.post(self.voice_server_url + "/accessToken", data=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        access_token = jwt.decode(r.text, verify=False)
        self.validate_access_token(access_token, identity)

    def validate_access_token(self, access_token, identity):
        self.assertTrue(access_token["sub"])
        self.assertTrue(access_token["iss"])
        self.assertTrue(access_token["exp"])
        self.assertTrue(access_token["grants"]["voice"])
        self.assertTrue(access_token["grants"]["identity"])
        self.assertEquals(identity, access_token["grants"]["identity"])

    def test_get_incoming(self):
        r = requests.get(self.voice_server_url + "/incoming")
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue("Congratulations" in r.text)

    def test_post_incoming(self):
        r = requests.post(self.voice_server_url + "/incoming")
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue("Congratulations" in r.text)

    def test_get_place_call(self):
        r = requests.get(self.voice_server_url + "/placeCall")
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue("CA" in r.text)

    def test_post_place_call(self):
        r = requests.post(self.voice_server_url + "/placeCall")
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue("CA" in r.text)

    def test_get_place_call_with_identity(self):
        identity = "bob"
        payload = {'to': identity}
        r = requests.get(self.voice_server_url + "/placeCall", params=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue("CA" in r.text)

    def test_post_place_call_with_identity(self):
        identity = "bob"
        payload = {'to': identity}
        r = requests.post(self.voice_server_url + "/placeCall", data=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue("CA" in r.text)

    def test_get_make_call(self):
        r = requests.get(self.voice_server_url + "/makeCall")
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue("Congratulations" in r.text)

    def test_post_make_call(self):
        r = requests.post(self.voice_server_url + "/makeCall")
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue("Congratulations" in r.text)

    def test_get_make_call_with_identity(self):
        identity = self.ALTERNATE_IDENTITY 
        payload = {'to': identity}
        r = requests.get(self.voice_server_url + "/makeCall", params=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue(self.DEFAULT_CALLER_ID in r.text)
        self.assertTrue(self.validate_identity_in_xml(identity, self.DEFAULT_CALLER_ID, r.text))

    def test_post_make_call_with_identity(self):
        identity = self.ALTERNATE_IDENTITY 
        payload = {'to': identity}
        r = requests.post(self.voice_server_url + "/makeCall", data=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue(self.DEFAULT_CALLER_ID in r.text)
        self.assertTrue(self.validate_identity_in_xml(identity, self.DEFAULT_CALLER_ID, r.text))

    def test_post_make_call_with_identity_starting_with_digit(self):
        identity = "0bob"
        payload = {'to': identity}
        r = requests.post(self.voice_server_url + "/makeCall", data=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue(self.DEFAULT_CALLER_ID in r.text)
        self.assertTrue(self.validate_identity_in_xml(identity, self.DEFAULT_CALLER_ID, r.text))

    def test_get_make_call_with_string_that_includes_plus_sign(self):
        identity = "12+345"
        payload = {'to': identity}
        r = requests.get(self.voice_server_url + "/makeCall", params=payload)
        print r.text
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue(self.DEFAULT_CALLER_ID in r.text)
        self.assertTrue(self.validate_identity_in_xml(identity, self.DEFAULT_CALLER_ID, r.text))

    def validate_identity_in_xml(self, identity, callerId, xml):
        simple_client_xml = "<Client>" + identity + "</Client>"
        dialer_client_xml = "<Client callerId=\"" + callerId + "\">" + identity + "</Client>"
        return simple_client_xml in xml or dialer_client_xml in xml

    def test_get_make_call_with_number(self):
        number = self.PHONE_NUMBER
        payload = {'to': number}
        r = requests.get(self.voice_server_url + "/makeCall", params=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue(self.DEFAULT_NUMBER_CALLER_ID in r.text)
        self.assertTrue(self.validate_number_in_xml(number, self.DEFAULT_NUMBER_CALLER_ID, r.text))

    def test_post_make_call_with_number(self):
        number = self.PHONE_NUMBER
        payload = {'to': number}
        r = requests.post(self.voice_server_url + "/makeCall", data=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue(self.DEFAULT_NUMBER_CALLER_ID in r.text)
        self.assertTrue(self.validate_number_in_xml(number, self.DEFAULT_NUMBER_CALLER_ID, r.text))

    def test_get_make_call_with_number_that_includes_plus_sign(self):
        number = "+12345"
        payload = {'to': number}
        r = requests.get(self.voice_server_url + "/makeCall", params=payload)
        self.assertEquals(requests.codes.ok, r.status_code)
        self.assertTrue(self.DEFAULT_NUMBER_CALLER_ID in r.text)
        self.assertTrue(self.validate_number_in_xml(number, self.DEFAULT_NUMBER_CALLER_ID, r.text))

    def validate_number_in_xml(self, number, callerId, xml):
        simple_number_xml = "<Number>" + number + "</Number>"
        dialer_number_xml = "<Number callerId=\"" + callerId + "\">" + number + "</Number>"
        return simple_number_xml in xml or dialer_number_xml in xml
