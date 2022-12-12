import os
from google.cloud import pubsub_v1
from flask import Flask, request

app = Flask(__name__)

service_account = "innovation2022.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(
    "innovation-2022", "wepay-clear-notifications")


@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        try:
            data = request.get_json()
            payload = data['data']
            topic_name = payload['topic']
            message = "WePay Clear Notification received with topic {}".format(
                topic_name)

            attributes = {
                "topicName": topic_name,
            }

            data = message.encode("utf-8")
            future = publisher.publish(topic_path, data, **attributes)
            print("Message published with ID: {}".format(future.result()))
        except Exception as e:
            print(e)
            return 'Error', 500
        return 'Success', 200


if __name__ == '__main__':
    app.run()
