Programmable Voice: Quickstart Application Server - Python
===
This repository contains the server-side web application required to run the [Twilio Programmable Voice iOS SDK Quickstart](https://www.twilio.com/docs/api/voice-sdk/ios/getting-started) and [Android SDK Quickstart](https://www.twilio.com/docs/api/voice-sdk/android/getting-started) mobile sample apps, written in Python.

Looking for the Quickstart mobile app?

Download the client-side Quickstart Applications in Swift and iOS here:

- [Swift Quickstart Mobile App](https://github.com/twilio/voice-quickstart-swift)
- [Objective-C Quickstart Mobile App](https://github.com/twilio/voice-quickstart-objc)

Download the client-side Quickstart Application for Android here:

- [Android Quickstart Mobile App](https://github.com/twilio/voice-quickstart-android)

Prerequisites
---

* A Twilio Account. Don't have one? [Sign up](https://www.twilio.com/try-twilio) for free!
* Follow the [iOS full quickstart tutorial here](https://www.twilio.com/docs/api/voice-sdk/ios/getting-started) or [Android full quickstart tutorial here](https://www.twilio.com/docs/api/voice-sdk/android/getting-started).

Up and running
---

This web application needs to be accessbile on the public internet in order to receive webhook requests from Twilio. Ngrok is a great options for getting this done quickly.

### Deploy locally using Python and [Ngrok](https://ngrok.com/)

For this option, you'll need to have the following tools installed on your development machine:

* [Python](https://www.python.org/) and `pip`
* [Ngrok](https://ngrok.com/)

Once you've got those, run the following command to install the required Python packages from within this project's parnet directory:

    pip install -r requirements.txt

Once that's done you can start the server by executing

    python server.py

And then, in a separate terminal window, make your server available to the public internet with the following:

    ngrok http 5000

You should see a dynamically generated public Ngrok URL in the command window. Ngrok will now tunnel all HTTP traffic directed at this URL to your local machine at port 5000.

There's one more step: Before the application server will work with _your_ Twilio account, you'll need to open the file `server.py` in your favorite text editor and replace `ACCOUNT_SID`, `API_KEY`, `API_KEY_SECRET`, `PUSH_CREDENTIAL_SID` and `APP_SID` with values from your Twilio account (Don't know what those values are? We cover this in detail in the [Programmable Voice iOS SDK Quickstart](https://www.twilio.com/docs/api/voice-sdk/ios/getting-started) and [Progammable Voice Android SDK Quickstart](https://www.twilio.com/docs/api/voice-sdk/android/getting-started).

### Deploy to the cloud using [Heroku](https://heroku.com)

Don't want to run the application server locally? You can also deploy it to the cloud using Heroku. Note: For this option, you'll want to gather your Twilio Account SID, API Key, API Key Secret, Push Credential SID and TwiML App SID before beginning the installation. (Don't know what these are? Read through the [Programmable Voice iOS SDK Quickstart](https://www.twilio.com/docs/api/voice-sdk/ios/getting-started) or [Programmable Voice Android SDK Quickstart](https://www.twilio.com/docs/api/voice-sdk/android/getting-started) for all the information.

If you don't already have one, visit Heroku and create a free account. Once that's done, click the button below to automatically set up this app, and enter the Twilio account information you gathered above when you're prompted.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Test the app
---

Test your app by opening the `/accessToken` endpoint in your browser (use the publicly accessible domain on Heroku or Ngrok, whichever you chose above). You should see a long string. This is an Access Token. You can examine its contents by pasting it into a JWT tool like [jwt.io](http://jwt.io).

Confused?
---

Read through the instructions in the [iOS Getting Started](https://www.twilio.com/docs/api/voice-sdk/ios/getting-started) or [Android Getting Started](https://www.twilio.com/docs/api/voice-sdk/android/getting-started) guides. Still having trouble? [Email us and we'll give you a hand.](mailto:help@twilio.com)

License
---
MIT
