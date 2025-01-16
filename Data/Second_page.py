# налаштування розміру вікна ківі
from kivy.core.window import Window

Window.size = (720, 550)  # розміри вікна

from kivy.uix.widget import Widget
from datetime import datetime
from kivy.uix.widget import ObjectProperty

import json
import random as rnd
# from Main_screens import dict_normu_zamiriv


# ---------- ДЛЯ РОЗМІЩЕННЯ КЛАСІВ НА ЕКРАНАХ-----------
# відкриття файлу з номами замірів
with open('Data\\json\\normu_zamiriv.json', 'r', encoding='utf-8') as normu_zamiriv:
    dict_normu_zamiriv = json.load(normu_zamiriv)


class Second_page(Widget):
    def vusota_protectora_shun(self, kategoria):
        print('kategoria_z_protector_shun= ', kategoria)
        try:
            if kategoria in ['M1', 'N1', 'O1', 'O2']:
                # print( rnd.randrange(dict_normu_zamiriv["vusota_protectora"][0][0],
                #                   dict_normu_zamiriv["vusota_protectora"][0][1])
                #
                # )
                return str(rnd.randrange(dict_normu_zamiriv["vusota_protectora"][0][0],
                                  dict_normu_zamiriv["vusota_protectora"][0][1]))

            if kategoria in ['M2','M3', 'N2', 'N3', 'O3', 'O4']:
                return str(rnd.randrange(dict_normu_zamiriv["vusota_protectora"][1][0],
                                  dict_normu_zamiriv["vusota_protectora"][1][1]))
            if kategoria in['', '-']:
                return '-'
        except Exception:
            pass

    def svitlopropuskania_vitrove(self):
        return str(rnd.randrange(dict_normu_zamiriv["svitlopropuskania"][0][0],
                                 dict_normu_zamiriv["svitlopropuskania"][0][1])
                   )
    def svitlopropuskania_bokove_zadnie(self):
        return str(rnd.randrange(dict_normu_zamiriv["svitlopropuskania"][1][0],
                                 dict_normu_zamiriv["svitlopropuskania"][1][1])
                   )
