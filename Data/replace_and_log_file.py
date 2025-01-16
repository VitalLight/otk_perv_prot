import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import json

from datetime import date
from pprint import pprint

from kivy.app import App

with open('Data\\json\\vumogu_otk.json', 'r', encoding='utf-8') as f_vumogu_otk:
    dict_f_vumogu_otk = json.load(f_vumogu_otk)

# відкриття файлу з шляхами до логотипів
with open('Data\\json\\path_to_img.json', 'r', encoding='utf-8') as path_to_img:
    dict_path_to_img = json.load(path_to_img)


class WordReplace:

    def __init__(self, dict_data, path_to_file_tmp, vin_code, path_to_folder_save):
        self.dict_data = dict_data
        self.path_to_file_tmp = path_to_file_tmp
        self.path_to_folder_save = path_to_folder_save
        self.vin_code = vin_code

    def open_file(self):
        # відкриття папки зі збереженими файлами
        os.startfile (self.path_to_folder_save)

    def save_file(self, docxTemplate_obj):
        # print("date", str(date.today().strftime("%d_%m_%Y")).replace("-", "_"))
        print("date", str(date.today().strftime("%d_%m_%Y")))
        try:  # збереження файлу
            docxTemplate_obj.save(self.path_to_folder_save + str(date.today().strftime("%d_%m_%Y"))+
                                  "_protokol_otk_" + f"{self.vin_code[0][-4:]}.docx")
            return docxTemplate_obj
        except Exception:
            return "error_save_file"

    def replace_data_in_file_and_save_it(self):
        # template_file_protokolu_otk.save(f"Data\doc\save\main_OTK_tmp_{self.vin_code[0][-4:]}_.docx")
        try:  # вносить в шаблон зміни
            print("in_replace_data_in_file_and_save_it")
            app = App.get_running_app()
            root = app.root

            # print("-----", root.screens[0].ids.first_page.ids.tg_b_ditu.state)

            template_file_protokolu_otk = DocxTemplate(self.path_to_file_tmp[0])

            # КЛЮЧИ ДЛЯ  ОСОБЛИВОСТІ КОНСТРУКЦІЇ
            d_image = {
                "tg_b_ditu":
                    InlineImage(template_file_protokolu_otk, dict_path_to_img['ditu'], width=Mm(10))
                    if root.screens[0].ids.first_page.ids.tg_b_ditu.state == "down" else "-",

                "tg_b_taxi": InlineImage(template_file_protokolu_otk, dict_path_to_img['taxi'], width=Mm(10))
                if root.screens[0].ids.first_page.ids.tg_b_taxi.state == "down" else "-",

                "tb_navchalnui": InlineImage(template_file_protokolu_otk, dict_path_to_img['navchalniy'], width=Mm(10))
                if root.screens[0].ids.first_page.ids.tb_navchalnui.state == "down" else "-",

                "tg_b_tumanka": InlineImage(template_file_protokolu_otk, dict_path_to_img['fog_front_light'],
                                            width=Mm(10))
                if root.screens[0].ids.first_page.ids.tg_b_tumanka.state == "down" else "-",

                "tg_b_negabarut": InlineImage(template_file_protokolu_otk, dict_path_to_img['negabarut'], width=Mm(10))
                if root.screens[0].ids.first_page.ids.tg_b_negabarut.state == "down" else "-",

                "tg_b_nebezpechniy": InlineImage(template_file_protokolu_otk, dict_path_to_img['nebezpechniy_vantag'],
                                                 width=Mm(10))
                if root.screens[0].ids.first_page.ids.tg_b_nebezpechniy.state == "down" else "-",

                "tg_b_cng": InlineImage(template_file_protokolu_otk, dict_path_to_img['cng'], width=Mm(10))
                if root.screens[0].ids.first_page.ids.tg_b_cng.state == "down" else "-",

                "tg_b_lpg": InlineImage(template_file_protokolu_otk, dict_path_to_img['lpg'], width=Mm(10))
                if root.screens[0].ids.first_page.ids.tg_b_lpg.state == "down" else "-"
            }

            # ОБНОВЛЯЄТСЬЯ СЛОВНИК КЛЮЧАМИ, ЩО ВІДПОВІДАЮТЬ ЗА ЗАБРАЖЕННЯ
            self.dict_data.update(d_image)  # для внесення всіх малюнкіцв

            # pprint(self.dict_data)

            # ЗДІЙСНЮЄТСЬЯ ЗАМІНА В ФАЙЛІ
            # ВНЕСЕННЯ САМИХ ВИМОГ ПЕРЕВІРКИ ТА РЕЗУЛЬТАТІВ ДО НИХ
            template_file_protokolu_otk.render(dict_f_vumogu_otk | self.dict_data)


            # ЗБЕРЕЖЕННЯ НОВОГО ФАЙЛУ ПІСЛЯ ЗАМІНИ ЗНАЧЕНЬ
            self.save_file(template_file_protokolu_otk)

        except Exception:
            return "ПОМИЛКА З ВНЕСЕННЯМ ЗМІН В ШАБЛОН ЧЕКУ В WordReplace"

        # ВІДКРИТТЯ ПАПКИ З ФАЙЛАМИ ПРОТОКОЛІВ ОТК
        self.open_file()
