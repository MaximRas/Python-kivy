import json
import requests
from modules import api_interface


# Класс описывающий методы работы с REST API. Наследуется от базового класса ApiInterface
class RestSettingsInterface(api_interface.ApiInterface):
    # Создает CryptoAPI адаптер для работы КриптоСервиса и добавляет его в БД
    def create_crypto_adapter(self, token, service_login, service_url, service_password):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        body = json.dumps({
            "Id": "CryptoAPI",  # смотреть в БД RestApiAdapterSettings название id уникальное для каждого адаптера
            "ApiConnectAddress": service_url,
            "ProxyMode": 0,
            "ProxyHost": "",
            "ProxyUserName": "",
            "ProxyUserPassword": "",
            "Login": service_login,
            "Password": service_password,
            "ExtendedLogging": True,
            "BinaryDataLogging": True
        })
        response = requests.post(self.url, data=body, headers=headers)
        return response.text
        # Создает CryptoAPI адаптер для работы КриптоСервиса и добавляет его в БД

    def create_archive_adapter(self, token, service_login, service_url, service_password):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        body = json.dumps({
            "Id": "Archive",  # смотреть в БД RestApiAdapterSettings название id уникальное для каждого адаптера
            "ApiConnectAddress": service_url,
            "ProxyMode": 0,
            "ProxyHost": "",
            "ProxyUserName": "",
            "ProxyUserPassword": "",
            "Login": service_login,
            "Password": service_password,
            "ExtendedLogging": True,
            "BinaryDataLogging": True
        })
        response = requests.post(self.url, data=body, headers=headers)
        return response.text

    # Добавляет КриптоСервис. Для того, чтобы все работало надо добавить также адаптер КриптоАПИ
    def add_crypto_service(self, token, element_id):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        body = json.dumps(
            {
                "Name": "CryptoServiceNative",
                "Id": element_id,
                # Включает галочку которая включает сервис для дотсупа к хранлищу сертификатов включен (имеется ввиду
                # что есть настройки CryptoAPI адаптера)
                "CertificateStoreServiceEnabled": True,
                # Включает шифрование и дешифрование данных
                "EncryptDecryptServiceEnabled": True,
                # Включает сервис для работы с электронными подписями
                "SignatureServiceEnabled": True,
                # Включает использование хранилища локального компьютера
                "UseLocalMachineStore": True
            })
        response = requests.post(self.url + "/CryptoServiceSettings", data=body, headers=headers)
        return response.text

    # Добавление сервиса архива
    def add_archive_service(self, token, type_bd='DB'):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        body = json.dumps(
            {
                "Name": "ArchiveDB",
                "Id": type_bd,
                "Enabled": True,
                "ExtendedLogging": True,
                "BinaryDataLogging": True
            })
        response = requests.post(self.url + "/CryptoServiceSettings", data=body, headers=headers)
        return response.text

    # Применении лицензии
    def apply_license(self, token, license_file_in_json):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        body = license_file_in_json
        response = requests.post(self.url + "/CryptoServiceSettings", data=body, headers=headers)
        return response.text

    # Добавить ящики по оператору. Важно! Метод будет работать один раз, т.к. можно добавить одного оператора на один ИМ
    # Если нужно обновить данные по оператору, то этот метод еще не разработан.
    def add_box(self, token, *args, **kwargs):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        body = json.dumps({
            # Нужно выяснить нюансы заполнения полей, пока оставлю пустым.
        })

        return None

    # Отправление документов
    def send_documents(self, token, document, operator_id, sender_id, receiver_id, meta_data, local_sign=False):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        if not local_sign:
            body = json.dumps({

            })
