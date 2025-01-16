# налаштування розміру вікна ківі
from kivy.core.window import Window

Window.size = (720, 550)  # розміри вікна

from kivy.uix.widget import Widget
from datetime import datetime
from kivy.uix.widget import ObjectProperty

import json
import random as rnd

from Data.First_page import First_page


# ---------- ДЛЯ РОЗМІЩЕННЯ КЛАСІВ НА ЕКРАНАХ-----------
# відкриття файлу з номами замірів
with open('Data\\json\\normu_zamiriv.json', 'r', encoding='utf-8') as normu_zamiriv:
    dict_normu_zamiriv = json.load(normu_zamiriv)

class Thrid_page(Widget):
    # obj_prop_id_kerm_luft = ObjectProperty(None)

    # відкриття файлу з номами замірів
    with open('Data\\json\\normu_zamiriv.json', 'r', encoding='utf-8') as normu_zamiriv:
        dict_normu_zamiriv = json.load(normu_zamiriv)

    # визначається сила світла фар в режимі ближнє світло в НЕосвітленій зоні і потім вставляється в kv файл
    liva_fara_NEosvitlena = str(rnd.randrange(dict_normu_zamiriv["blugni_faru_NEosvitlena"][0],
                                              dict_normu_zamiriv["blugni_faru_NEosvitlena"][1],
                                              dict_normu_zamiriv["blugni_faru_NEosvitlena"][2]
                                              )
                                )

    prava_fara_NEosvitlena = str(rnd.randrange(dict_normu_zamiriv["blugni_faru_NEosvitlena"][0],
                                               dict_normu_zamiriv["blugni_faru_NEosvitlena"][1],
                                               dict_normu_zamiriv["blugni_faru_NEosvitlena"][2]
                                               )
                                 )
    # визначається сила світла фар в режимі ближнє світло в освітленій зоні і потім вставляється в kv файл

    liva_fara_osvitlena = str(rnd.randrange(dict_normu_zamiriv["blugni_faru_osvitlena"][0],
                                            dict_normu_zamiriv["blugni_faru_osvitlena"][1],
                                            dict_normu_zamiriv["blugni_faru_osvitlena"][2]
                                            )
                              )
    prava_fara_osvitlena = str(int(str(int(liva_fara_osvitlena) * rnd.uniform(.95, 1.05))[:2]) * 100)

    # визначається сила світла фар в режимі дальнє світло
    liva_fara_dalna = str(rnd.randrange(dict_normu_zamiriv["dalni_faru"][0],
                                    dict_normu_zamiriv["dalni_faru"][1],
                                    dict_normu_zamiriv["dalni_faru"][2]
                                    ))
    prava_fara_dalna = str(int(liva_fara_dalna) * rnd.uniform(.90, 1.10))[:3]+"00"

    #  сума сил світла дальніх фар
    liva_plus_prava_fara_dalna = int(liva_fara_dalna) + int(prava_fara_dalna)

    #  сума сил світла туманних фар
    liva_tumanka = str(rnd.randrange(dict_normu_zamiriv["tumanni_faru"][0],
                                     dict_normu_zamiriv["tumanni_faru"][1],
                                     dict_normu_zamiriv["tumanni_faru"][2]
                                     )
                       )

    prava_tumanka = str(rnd.randrange(dict_normu_zamiriv["tumanni_faru"][0],
                                      dict_normu_zamiriv["tumanni_faru"][1],
                                      dict_normu_zamiriv["tumanni_faru"][2])
                        )


    def luft_kolis(self, kategoria):
        print("kategoria_z_luftu_kolis= ", kategoria)

        try:
            if kategoria in ['M1', 'M2', 'N1']:
                return str(rnd.randrange(
                    dict_normu_zamiriv["luft_kerma"][0][0],
                    dict_normu_zamiriv["luft_kerma"][0][1],
                    dict_normu_zamiriv["luft_kerma"][0][2],
                )
                )

            if kategoria in ['M3', 'N2', 'N3']:
                return str(rnd.randrange(
                    dict_normu_zamiriv["luft_kerma"][1][0],
                    dict_normu_zamiriv["luft_kerma"][1][1],
                    dict_normu_zamiriv["luft_kerma"][1][2],
                )
                )

            if kategoria in ['', '-', 'O1', '02', '03', '04']:
                return "-"

        except Exception:
            pass


    pass
