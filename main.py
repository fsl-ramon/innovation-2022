import os
import json
from signature_verifier import WePayClearSignatureVerifier
from google.cloud import pubsub_v1
from flask import Flask, request

app = Flask(__name__)

service_account = "innovation2022.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account

wepay_clear_client_id = "850142"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(
    "innovation-2022", "wepay-clear-notifications")

# load public key
with open("pubkey.pem", "rb") as f:
    public_key = f.read()


@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        try:
            request_json = request.get_json()
            data = request_json['data']
            signature = request.headers['wepay-signature']
            payload = data['payload']
            # check data.topic attribute
            if not data['topic']:
                return 'Error', 200

            # validate client id in payload
            if data["owner"]["id"] != wepay_clear_client_id:
                return 'Invalid client ID', 200

            # validate signature in header
            if not signature:
                return 'Missing signature', 200
            else:
                # verify request signature
                verifier = WePayClearSignatureVerifier(public_key)
                if not verifier.verify_signatures(data, signature):
                    return 'Invalid signature', 200

            # seems 'topic' is a reserved word in PubSub attributes
            data['topic_name'] = data.pop('topic')

            topic_name = data['topic_name']
            message = "WePay Clear Notification received with topic {}".format(
                topic_name)

            title = message.encode("utf-8")
            attributes = {
                "topic_name": topic_name,
                "payload": json.dumps(payload),
            }

            future = publisher.publish(topic_path, title, **attributes)
            print("Message published with ID: {}".format(future.result()))
        except Exception as e:
            print(e)
            return 'Error', 200
        return 'Success', 200


if __name__ == '__main__':
    app.run()
