import requests
import json


'''Общий класс для описания API интерфейса
включает в себя все общие методы, которые есть в сервисах
'''
class ApiInterface:

    def __init__(self, url, password, login):
        self.url = url
        self.password = password
        self.login = login

    def authorization(self):
        header = {'Content-type': 'application/json'}
        body = json.dumps({"Username": self.login, "Password": self.password})
        get_token = requests.post(self.url + '/token', data=body, headers=header)

        return get_token.json()['access_token']
