import http.client
import ssl
import json


class ACI:

    def __init__(self):
        self.__connection = None
        self.__headers = None
        self.__username = None

    def connect(self, hostname, username, password):
        self.__username = username
        body = {'aaaUser': {'attributes': {'name': username, 'pwd': password}}}
        ssl_context = ssl.SSLContext()
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.check_hostname = False
        self.__connection = http.client.HTTPSConnection(host=hostname, context=ssl_context)
        self.__connection.request(method='POST', url='/api/aaaLogin.json', body=json.dumps(body))
        response = self.__connection.getresponse()
        result = response.read()
        if response.status == 200:
            decoded_json = json.loads(result)
            token = decoded_json['imdata'][0]['aaaLogin']['attributes']['token']
            self.__headers = {'cookie': 'APIC-cookie=' + token}
            return True
        else:
            return False

    def disconnect(self):
        if self.__headers:
            body = {'aaaUser': {'attributes': {'name': self.__username}}}
            self.method_post(url='/api/aaaLogout.json', body=json.dumps(body))
        self.__connection.close()
        self.__connection = None
        self.__headers = None
        self.__username = None

    def token_refresh(self):
        result = self.method_get(url='/api/aaaRefresh.json')
        if result:
            token = result['imdata'][0]['aaaLogin']['attributes']['token']
            self.__headers = {'cookie': 'APIC-cookie=' + token}

    def method_get(self, url):
        self.__connection.request(method='GET', url=url, headers=self.__headers)
        response = self.__connection.getresponse()
        result = response.read()
        if response.status == 200:
            return json.loads(result)
        else:
            return None

    def method_post(self, url, body):
        self.__connection.request(method='POST', url=url, body=body, headers=self.__headers)
        response = self.__connection.getresponse()
        result = response.read()
        if response.status == 200:
            return json.loads(result)
        else:
            return None

    def method_delete(self, url):
        self.__connection.request(method='DELETE', url=url, headers=self.__headers)
        response = self.__connection.getresponse()
        result = response.read()
        if response.status == 200:
            return json.loads(result)
        else:
            return None
