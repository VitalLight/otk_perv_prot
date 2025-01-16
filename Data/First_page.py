# налаштування розміру вікна ківі
from kivy.core.window import Window

Window.size = (720, 550)  # розміри вікна

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
import json

from kivy.uix.popup import Popup


# ---------- ДЛЯ РОЗМІЩЕННЯ КЛАСІВ НА ЕКРАНАХ-----------

class First_page(Widget):
    #     для визначення вибраної категорії в змінну

    # відкриття файлу з нормами замірів
    with open('Data\\json\\normu_zamiriv.json', 'r', encoding='utf-8') as normu_zamiriv:
        dict_normu_zamiriv = json.load(normu_zamiriv)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def date_(self, data_):
        paste_data = f'{data_[:2]}.{data_[2:4]}.{data_[4:]}'
        return paste_data

    def vantagnist(self, povna_masa, sporiadgena_masa):

        if povna_masa.isnumeric() is False or sporiadgena_masa.isnumeric() is False:
            return ""

        try:
            " Перевіряємо внесені показники мас чи во є числами "
            povna_masa.isnumeric()
            sporiadgena_masa.isnumeric()

            if int(povna_masa) > int(sporiadgena_masa):
                return str(int(int(povna_masa) - int(sporiadgena_masa)) / 1000)

            if int(povna_masa) < int(sporiadgena_masa):
                return 'p_m<s_m!!!'

        except Exception:
            pass

    def for_paste_picture_in_doc_file(self, tb_id, path_to_image):
        print(tb_id.state)
        if tb_id.state == 'down':
            return path_to_image

    def upper_string(self, text):
        return str(text).upper()

    def move_to_second_page_if_katrgoria_check(self):
        app = App.get_running_app()
        root = app.root

        variable_screen = root.get_screen('first_page_screen').ids.first_page.ids

        if variable_screen.ti_vin_code.text != "" and \
                variable_screen.ti_derj_nomer.text != "" and \
                variable_screen.ti_seria_tehpasportu.text != "" and \
                variable_screen.sp_kategoria.text != "-":
            root.get_screen('first_page_screen').manager.current = "second_page_screen"
            root.get_screen('first_page_screen').manager.transition.direction = "left"

        else:
            attaction_text = """ 
            ПОЛЯ - ВІН-КОД, ДЕРЖ.НОМЕР, СЕРІЯ НОМЕР ТЕХПАСПОРТУ, КАТЕГОРІЯ КТЗ  -  МАЮТЬ БУТИ ЗАПОВНЕННІ !!!
             """
            # text_size = (self.width, None)
            obj_zapovnit_polia  =Popup(title="ЗВЕРНІТЬ УВАГУ НА ПОЛЯ",
                  content=Label(text= attaction_text, text_size = (350, None), color  = '#aab624'),
                  #auto_dismiss=False,
                  # By default, any click outside the popup will dismiss/close it. If you don't want that, you can set
                  size_hint=(None, None),
                  size=(400, 200)
                  )
            'ВІДКРИВАЄ ВІКНО З ІНФО ПРО НЕ ЗАПОВНЕННІ ПОЛЯ'
            obj_zapovnit_polia.open()

