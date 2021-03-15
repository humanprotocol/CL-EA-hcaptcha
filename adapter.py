from bridge import Bridge


class Adapter:
    base_url = 'https://hcaptcha.com/siteverify'
    token = None
    secret_key = None

    def __init__(self, input, secret_key: str=None):
        self.id = input.get('id', '1')
        self.secret_key = secret_key
        self.request_data = input.get('data')
        if self.validate_request_data() and self.secret_key:
            self.bridge = Bridge()
            self.set_params()
            self.create_request()
        else:
            self.result_error('No data or API secret key provided for the adapter')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def set_params(self):
        self.token = self.request_data.get('token')

    def create_request(self):
        try:
            data = f'response={self.token}&secret={self.secret_key}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = self.bridge.post_request(self.base_url, data=data, headers=headers)
            data = response.json()
            print('Response: ', data)
            self.result = data['success']
            data['result'] = self.result
            self.result_success(data)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': self.result,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
