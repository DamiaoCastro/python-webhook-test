import re
from google.cloud import pubsub_v1
from flask import Flask, request
import os
PUBSUB_TOPIC_VAR_NAME = "PUBSUB_TOPIC"
topic_path = os.environ.get(PUBSUB_TOPIC_VAR_NAME)

if len(topic_path) == 0:
    raise Exception(
        'Environment variable "{PUBSUB_TOPIC_VAR_NAME}" is not defined')

match = re.search("^projects\/[^/]+\/topics\/[^/]+$", topic_path)
if match is None:
    raise Exception(
        'Environment variable "{PUBSUB_TOPIC_VAR_NAME}" does NOT have the expected format')

app = Flask(__name__)
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT',
                'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

publisher = pubsub_v1.PublisherClient()


@app.route('/', defaults={'path': ''}, methods=HTTP_METHODS)
@app.route('/<path:path>', methods=HTTP_METHODS)
def catch_all(path):

    payload = request.get_data(
        cache=False, as_text=False, parse_form_data=False)

    if len(payload) > 0:

        dictionary = {}
        for itemKey in request.headers.keys():
            dictionary[itemKey] = request.headers[itemKey]
        dictionary['request-path'] = request.path
        dictionary['request-method'] = request.method

        future = publisher.publish(topic_path, payload, **dictionary)
        try:
            future.result()
        except:
            return ('ERROR', 500)

    return ('OK', 200)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
