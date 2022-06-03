import requests
import json
from modules import api_interface


# Класс описывающий сервис архива и его методы.
# Наследуется из основного класса ApiInterface
class ArchiveInterface(api_interface.ApiInterface):
    """Сохранение файла в архив.
    Метод принимает в json имя, тип, guid документа, а содержание файла
    в text/plain в бинарном виде.
    """
    def save_files_to_archive(self, file_in_byte, token, files):
        headers = {'Authorization': 'Bearer ' + token}
        body = {
            "json": (None, files, "application/json"),
            "content": file_in_byte
        }
        response = requests.post(self.url + '/archive', files=body, headers=headers)
        return response.text
    """Выгрузка файла из архива.
    Выгружает из архива файл с заданной ссылкой. 
    """
    def load_files_from_archive(self, link_to_file, token):
        headers = {'Authorization': 'Bearer ' + token}
        response = requests.get(self.url + '/archive/' + link_to_file, headers=headers)
        with open('./file_from_archive' + link_to_file, 'w') as f:
            f.write(response.text)
        return response.text
