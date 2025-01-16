# налаштування розміру вікна ківі
from kivy.core.window import Window

Window.size = (720, 550)  # розміри вікна

from kivy.uix.widget import Widget

import json

# відкриваємо файл з персоналом
with open('Data\\json\\personal.json', encoding='utf-8') as personal:
    dict_personal = json.load(personal)



# ---------- ДЛЯ РОЗМІЩЕННЯ КЛАСІВ НА ЕКРАНАХ-----------

class Nalashtuvania_page(Widget):
    # -----------відкриваємо файл з інфо про лабораторію___
    with open('Data\\json\\info_about_dilnuci_lv.json', encoding='utf-8') as info_about_lv:
        dict_info_about_lv = json.load(info_about_lv)

    def input_personal_active_disactive(self, id_togglebutton, id_textinput, btn_add_remove_save, input_person):
        if id_togglebutton.state == 'normal':
            id_textinput.disabled = True
            btn_add_remove_save.disabled = True

            input_person.disabled = True

        if id_togglebutton.state == 'down':
            id_textinput.disabled = False
            btn_add_remove_save.disabled = False

            input_person.disabled = True

    @staticmethod
    def btn_add_person(id_input_kerivnuka, id_input_ingenera, sp_kerivnuku, sp_first_engineer, sp_second_engineer):
        # ВІДКРИВАЄМО ФАЙЛ І
        # with open('Data\\json\\personal.json', encoding='utf-8') as personal:
        #     dict_personal = json.load(personal)

        # ВНОСИМО В СЛОВНИК ЗМІНИ
        if id_input_kerivnuka.disabled is False and id_input_ingenera.disabled is True:
            dict_personal['list_kerivnuku'].insert(0, f"{id_input_kerivnuka.text}")  # ДОБАВЛЕННЯ ЕЛЕМЕНТІВ ДО СПИСКУ

            dict_personal.update({'list_kerivnuku': dict_personal['list_kerivnuku']})  # ОНОВЛЕННЯ СЛОВНИКА
            id_input_kerivnuka.text = ""  # Очищення поля
            # id_input_ingenera.text = ""  # Очищення поля
            sp_kerivnuku.values = dict_personal['list_kerivnuku']

        if id_input_ingenera.disabled is False and id_input_kerivnuka.disabled is True:
            dict_personal['list_ingeneru'].insert(0, f"{id_input_ingenera.text}")  # ДОБАВЛЕННЯ ЕЛЕМЕНТІВ ДО СПИСКУ

            dict_personal.update({'list_ingeneru': dict_personal['list_ingeneru']})  # ОНОВЛЕННЯ СЛОВНИКА
            # id_input_kerivnuka.text = ""  # Очищення поля
            id_input_ingenera.text = ""  # Очищення поля

            sp_first_engineer.values = sp_second_engineer.values = dict_personal['list_ingeneru']
            # sp_second_engineer.values = dict_personal['list_ingeneru']

        # ЗАПИС ДО ТОГО Ж ФАЙЛУ ЗМІН / ОНОВЛЕННЯ ДАНИХ
        json.dump(dict_personal,
                  open('Data\\json\\personal.json', 'w+', encoding='utf-8'),
                  ensure_ascii=False,  # залишить форматування без змін
                  indent=4)

    @staticmethod
    def btn_remove_person(id_input_kerivnuka, id_input_ingenera, sp_kerivnuku, sp_first_engineer, sp_second_engineer):
        try:
            if id_input_kerivnuka.disabled is False and id_input_ingenera.disabled is True:
                dict_personal['list_kerivnuku'].remove(f"{id_input_kerivnuka.text}")  # ДОБАВЛЕННЯ ЕЛЕМЕНТІВ ДО СПИСКУ
                dict_personal.update({'list_kerivnuku': dict_personal['list_kerivnuku']})  # ОНОВЛЕННЯ СЛОВНИКА
                id_input_kerivnuka.text = ""  # Очищення поля
                id_input_ingenera.text = ""  # Очищення поля
                sp_kerivnuku.values = dict_personal['list_kerivnuku']

            if id_input_ingenera.disabled is False and id_input_kerivnuka.disabled is True:
                dict_personal['list_ingeneru'].remove(f"{id_input_ingenera.text}")  # ДОБАВЛЕННЯ ЕЛЕМЕНТІВ ДО СПИСКУ
                dict_personal.update({'list_ingeneru': dict_personal['list_ingeneru']})  # ОНОВЛЕННЯ СЛОВНИКА
                id_input_kerivnuka.text = ""  # Очищення поля
                id_input_ingenera.text = ""  # Очищення поля
                sp_first_engineer.values = dict_personal['list_ingeneru']
                sp_second_engineer.values = dict_personal['list_ingeneru']

        except Exception:
            pass

        # ЗАПИС ДО ТОГО Ж ФАЙЛУ ЗМІН
        json.dump(dict_personal,
                  open('Data\\json\\personal.json', 'w+', encoding='utf-8'),
                  ensure_ascii=False,
                  indent=4)
        pass

    @staticmethod
    def btn_save_change_in_file_pesonal(sp_kerivnuku, sp_first_engineer, sp_second_engineer):
        # збереження керівника
        if len(dict_personal['kerivnuk']) < 1:
            dict_personal['kerivnuk'].append(sp_kerivnuku.text)
        else:
            dict_personal['kerivnuk'][0] = sp_kerivnuku.text

        # збереження інженерів що проводили випробування
        if len(dict_personal['ingeneru_vukonavci']) < 2:
            dict_personal['ingeneru_vukonavci'].append(sp_first_engineer.text)
            dict_personal['ingeneru_vukonavci'].append(sp_second_engineer.text)
        else:
            dict_personal['ingeneru_vukonavci'][0] = sp_first_engineer.text
            dict_personal['ingeneru_vukonavci'][1] = sp_second_engineer.text

        # ЗАПИС ДО ТОГО Ж ФАЙЛУ ЗМІН
        json.dump(dict_personal,
                  open('Data\\json\\personal.json', 'w+', encoding='utf-8'),
                  ensure_ascii=False,
                  indent=4)
    # ----------------------------

    def insert_info_about_lv(self):

        self.dict_info_about_lv.update(
            { "lv_name": self.ids.lv_name.text,
              "lv_adressa": self.ids.lv_adressa.text,
              "lv_atestat": self.ids.lv_atestat.text,
              "adressa_vuprobuvan": self.ids.adressa_vuprobuvan.text,
              "nomer_v_gsc": self.ids.nomer_v_gsc.text,
              'nomer_dilnuci': self.ids.nomer_dilnuci.text

             }
        )

        # ЗАПИС ДО ТОГО Ж ФАЙЛУ ЗМІН
        json.dump(self.dict_info_about_lv,
                  open('Data\\json\\info_about_dilnuci_lv.json', 'w+', encoding='utf-8'),
                  ensure_ascii=False, #  це щоб не було форматування
                  indent=4
                  )
