import os
from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():

#  request_secret = request.headers['Secret']
#     if request_secret != os.environ['SECRET']:
#         return ('Unauthorized', 401)    

    # data = request.get_json()

    return ('OK', 200)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))