from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader, TabbedPanelItem, TabbedPanelStrip
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.sandbox import Sandbox
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from modules import api_interface
from modules import archive_interface
from modules import rest_interface
import requests
import urllib.request

#  Настройка разрешения окна и убирание фона у окна
Window.size = (1250, 800)
Window.clearcolor = (1, 1, 1, 1)


# Проверка что заданный адрес возвращает нам код 200 или 302(перенапраление на сваггер)
def url_checker(url):
    status_code = 0
    try:
        check_url = requests.head(url)
        if check_url.status_code == 200 or check_url.status_code == 302 or url != '':
            return '200'
        else:
            status_code = check_url.status_code
            return 'Connection error ' + str(status_code)
    except requests.exceptions.RequestException:
        return 'Connection error ' + str(status_code)


# Класс описывающий интерфейс и свойства возникновения ошибок при взаимодействии с UI
class Alert(Popup):

    def __init__(self, title, text):
        super(Alert, self).__init__()
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')
        content.add_widget(
            Label(text=text, halign='left', valign='top')
        )
        ok_button = Button(text='Ok', size_hint=(None, None), size=(Window.width / 15, Window.height / 15))
        content.add_widget(ok_button)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(Window.width / 2, Window.height / 4),
            auto_dismiss=True,
        )
        ok_button.bind(on_press=popup.dismiss)
        popup.open()


# функция которая проверяет соединение и вызывает класс Alert при ошибке
# т.к. не все ошибки требуют вызова алерт функцию проверки url url_checker() не надо обеъединять с этой функцией.
def connection_test(url_id):
    try:
        status_code = url_checker(url_id)
        if status_code != '200' or status_code == '':
            raise ValueError
        return url_id
    except ValueError:
        status_code = url_checker(url_id)
        Alert('Value Error!', 'Connection to  ' + url_id + " returned " + status_code)
        return 'Error'


""" 
Класс описиывающий меню с вкладками на основном интерфейсе. 
Содерижит в себе все параметры и является способом взаимодейсвтия пользователя с логикой.
Параметры и свойсва беруться из файла loader.kv
Используется фреймворк kivy и его библиотеки для создания классов и виджетов интерфейса
"""


class Tab(TabbedPanel):
    check_box_innkpp = ObjectProperty(None)
    check_box_boxid = ObjectProperty(None)

    def send(self):
        spinner_id = self.ids.spinner_of_api.text

        if spinner_id == 'REST':
            rest_api = self.ids.rest_connection.text
            connection_test(rest_api)
        if spinner_id == 'SOAP':
            soap_api = self.ids.soap_connection.text
            connection_test(soap_api)
        archive_api = self.ids.archive_connection.text
        connection_test(archive_api)
        crypto_api = self.ids.crypto_connection.text
        connection_test(crypto_api)

        # Блок чтения параметров из чекбоксов
        soap_api = self.ids.soap_connection.text
        upd_kscf_dop = self.ids.upd_kscf_dop.active
        upd_kscf = self.ids.upd_kscf.active
        upd_scf = self.ids.upd_scf.active
        ukd_kscf_dop = self.ids.ukd_kscf_dop.active
        ukd_kscf = self.ids.ukd_kscf.active
        ukd_scf = self.ids.ukd_scf.active
        upd_kscf_dop_pros = self.ids.upd_kscf_dop_pros.active
        upd_kscf_pros = self.ids.upd_kscf_pros.active
        upd_scf_pros = self.ids.upd_scf_pros.active
        ukd_kscf_dop_pros = self.ids.ukd_kscf_dop_pros.active
        ukd_kscf_pros = self.ids.ukd_kscf_pros.active
        ukd_scf_pros = self.ids.ukd_scf_pros.active
        upd_kscf_dop_mark = self.ids.upd_kscf_dop_mark.active
        upd_kscf_mark = self.ids.upd_kscf_mark.active
        upd_scf_mark = self.ids.upd_scf_mark.active
        ukd_kscf_dop_mark = self.ids.ukd_kscf_dop_mark.active
        ukd_kscf_mark = self.ids.ukd_kscf_mark.active
        ukd_scf_mark = self.ids.ukd_scf_mark.active


# Класс описывающий общее окно, которое создается при запуске приложения.
# Наследуется из класса App, который генерирует окно
class LoaderApp(App):

    # Специальный метод фреймворка, которые создает окно.
    # Должен возвращать лейаут (слой) который будет показан первым

    def build(self):
        layout = GridLayout(orientation='tb-lr')
        layout.cols = 1
        layout.add_widget(Tab())

        return layout


if __name__ == '__main__':
    LoaderApp().run()
