import os
from flask import Flask, request, jsonify

from adapter import Adapter

app = Flask(__name__)

secret_key = os.environ.get('HCAPTCHA_SECRET_KEY', '0xEf618286496e03c9621C8B6a287569bC4d212dBA')
env = os.environ.get('PYENV', 'dev')

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
    app.run(debug=True if env == 'dev' else False, host='0.0.0.0', port='8080', threaded=True)
