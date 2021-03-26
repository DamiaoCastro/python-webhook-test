import os
from flask import Flask, request
from google.cloud import pubsub_v1
app = Flask(__name__)

project_id = "damiao-project-1" #os.environ.get("project_id")
topic_id = "webhook-test-1" #os.environ.get("topic_id")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

@app.route('/', methods=['POST'])
def index():

    #  request_secret = request.headers['Secret']
    #     if request_secret != os.environ['SECRET']:
    #         return ('Unauthorized', 401)   

    payload = request.get_data(cache=False, as_text=False, parse_form_data=False)

    future = publisher.publish(topic_path, payload, p1='p2')
    try:
        future.result()
    except:
        return ('ERROR', 500)

    return ('OK', 200)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))