import os
from flask import Flask, request, jsonify

from adapter import Adapter

app = Flask(__name__)

secret_key = os.environ.get('HCAPTCHA_SECRET_KEY', '0x6BEAa0fD14148A7b46b5151E1460D86826D40fc6')
env = os.environ.get('PYENV', 'dev')
port = os.environ.get('PORT', 8080)

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/', methods=['POST'])
def call_adapter():
    data = request.get_json()
    if data == '':
        data = {}
    adapter = Adapter(data, secret_key=secret_key)
    return jsonify(adapter.result)


if __name__ == '__main__':
    app.run(debug=True if env == 'dev' else False, host='0.0.0.0', port=port, threaded=True)
