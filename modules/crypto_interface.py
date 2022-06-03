import requests
import json
from modules import api_interface


# Класс опиывающий методы КриптоАПИ.
# Наследуется из основного класса ApiInterface
class CryptoInterface(api_interface.ApiInterface):
    """Подписать содержимое.
    Подписывает заднный контент указанным сертификатом. Может одновременно несколько
    документов подписать. Метод принимает на вход отпечаток сертификата.
    Даные передаются в json
    """
    def create_sign(self, token, thumbprint, contents, include_errors=True):
        if isinstance(contents, list):
            for i in contents:
                contents[i] = i.encode('base64')
        else:
            content = contents.encode('base64')

        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        body = json.dumps({"Thumbprint": thumbprint,
                           "ThrowOnErrors": include_errors,
                           "Contents": contents
                           })
        response = requests.post(self.url + "/v2/sign", data=body, headers=headers)

        return response.text
    """Валидаия содержимого.
    Валидирует содержимое контента на соответствие переданной подписи.
    Данные передаются в json
    """
    def validate(self, token, contents, signature, default_on_fail=True, verify_signature_only=True):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        body = json.dumps({
            "Content": contents,
            "Signature": signature,
            "DefaultOnFail": default_on_fail,
            "VerifySignatureOnly": verify_signature_only
        })
        response = requests.post(self.url + '/v2/validate', data=body, headers=headers)
        return response.text
    """Получить сертификат.
    Возвращает данные сертификата (с ключом либо без) в виде base64. 
    Даные возвращаются в json
    """
    def get_certificate(self, token, thumbprint, has_private_key=True):
        headers = {'Content-type': 'application/octet-stream', 'Authorization': 'Bearer ' + token}
        response = requests.get(self.url + "/certificates/" + thumbprint, params=has_private_key)
        return response.text
    """Получить список сертификатов.
    Возвращает список доступных (непросроченный) сертификатов(только открытую часть). 
    Даные возвращаются в json
    """
    def get_certificates(self, token):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        response = requests.get(self.url + "certificates")
        return response.text
    """Улучшить подпись.
    Улучшает переданную подпись(если возможно). В ответ вернется улучшенная подпись в json
    """
    def enhance_sign(self, token, signature):
        headers = {'Content-type': 'application/octet-stream', 'Authorization': 'Bearer ' + token}
        body = json.dumps(signature)
        response = requests.post(self.url + "/enhance", data=body, headers=headers)
        return response.text
    """Зашифровать данные.
    Шифрует контент при помощи заданной подписи. Если передан параметр CertificateRawData,
    то параметр "Thumbprint" игнорируется.
    """
    def encrypt_data(self, token, content, thumbprint=None, certificate_raw_data=None):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        if certificate_raw_data is not None:
            body = json.dumps({
                "CertificateRawData": certificate_raw_data,
                "ThrowOnErrors": True,
                "Contents": content
            })
        else:
            body = json.dumps({
                "Thumbprint": thumbprint,
                "ThrowOnErrors": True,
                "Contents": content
            })
        response = requests.post(self.url + "/v2/encrypt", data=body, headers=headers)
        return response.text
    """Расшифровать данные.
    Расшифрует контент, который был зашифрован при помощи сертификата. 
    Если нету сертификата для расшифрования, вернеться ошибка
    """
    def decrypt_data(self, token, content):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        body = json.dumps({
            "EncryptedContent": content,
            "DefaultOnFail": True
        })
        response = requests.post(self.url + "/decrypt", data=body, headers=headers)
        return response.text
