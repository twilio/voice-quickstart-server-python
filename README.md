Programmable Voice: Quickstart Application Server - Python
===
This repository contains the server-side web application required to run the [Twilio Programmable Voice iOS SDK Quickstart](https://www.twilio.com/docs/api/voice-sdk/ios/getting-started) and [Android SDK Quickstart](https://www.twilio.com/docs/api/voice-sdk/android/getting-started) mobile sample apps.

Looking for the Quickstart mobile app?

Download the client-side Quickstart Applications in Swift and iOS here:

- [Swift Quickstart Mobile App](https://github.com/twilio/voice-quickstart-swift)
- [Objective-C Quickstart Mobile App](https://github.com/twilio/voice-quickstart-objc)

Download the client-side Quickstart Application for Android here:

- [Android Quickstart Mobile App](https://github.com/twilio/voice-quickstart-android)

## Prerequisites

* A Twilio Account. Don't have one? [Sign up](https://www.twilio.com/try-twilio) for free!
* Follow the [iOS full quickstart tutorial here](https://www.twilio.com/docs/api/voice-sdk/ios/getting-started) or [Android full quickstart tutorial here](https://www.twilio.com/docs/api/voice-sdk/android/getting-started).

## Setting up the Application

Open the file `server.py`. Edit `ACCOUNT_SID`, `API_KEY`, `API_KEY_SECRET` with the values gathered above in the Android or iOS quickstart.

Next, install `pip` on your machine:

* [Python](https://www.python.org/) and `pip`

Once installed run the following command to install the required Python packages from within this project's parent directory:

    pip install -r requirements.txt

Once that's done you can start the server by executing:

    python server.py

Visit [http://localhost:5000](http://localhost:5000) to ensure the server is running.

### Up and running

This web application needs to be accessbile on the public internet in order to receive webhook requests from Twilio. [Ngrok](https://ngrok.com/) is a great options for getting this done quickly.

Once you have the application running locally, in a separate terminal window, make your server available to the public internet with the following:

    ngrok http 5000

You should see a dynamically generated public Ngrok URL in the command window. Ngrok will now tunnel all HTTP traffic directed at this URL to your local machine at port 5000.

### Test the app

Test your app by opening the `{YOUR_SERVER_URL}/accessToken` endpoint in your browser. Use the publicly accessible domain on ngrok. You should see a long string. This is an Access Token. You can examine its contents by pasting it into a JWT tool like [jwt.io](http://jwt.io).

## License

MIT
