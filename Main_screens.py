import sys
import os
import json
from PIL import Image

from Data.replace_and_log_file import WordReplace

from pprint import pprint
from docxtpl import DocxTemplate, InlineImage

from datetime import date
# налаштування розміру вікна ківі
from kivy.core.window import Window

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.spinner import Spinner
from kivy.uix.spinner import SpinnerOption

import random as rnd
# завантаження сторінок------------------------
from Data.First_page import First_page
from Data.Second_page import Second_page
from Data.Thrid_page import Thrid_page
from Data.Four_page import Four_page
from Data.Fifth_page import Fifth_page
from Data.Nalashtuvania_page import Nalashtuvania_page
# ----------------------------------
from datetime import datetime


from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, \
    SlideTransition  # ДЛЯ створення різних екранів

""" відкриватимуться файли з інформацією для створення протоколу"""
# відкриття файлу з вимогами протоколу ОТК
with open('Data\\json\\vumogu_otk.json', 'r', encoding='utf-8') as f_vumogu_otk:
    dict_f_vumogu_otk = json.load(f_vumogu_otk)
# print(dict_f_vumogu_otk['tak_ni_ns'])

# відкриття файлу з інформацією про дільницю ЛВ
with open('Data\\json\\info_about_dilnuci_lv.json', 'r', encoding='utf-8') as info_about_dilnuci_lv:
    dict_info_about_dilnuci_lv = json.load(info_about_dilnuci_lv)

# відкриття файлу з шляхами до логотипів
with open('Data\\json\\path_to_img.json', 'r', encoding='utf-8') as path_to_img:
    dict_path_to_img = json.load(path_to_img)

# відкриття файлу з персоналом
with open('Data\\json\\personal.json', 'r', encoding='utf-8') as personal:
    dict_personal = json.load(personal)

    # заповнення словника якщо кількість керівників <1
    if len(dict_personal['kerivnuk']) < 1:
        while len(dict_personal['kerivnuk']) < 1:
            dict_personal['kerivnuk'].append(" ")

        # заповнення словника якщо кількість інженерів виконвців  <2
        if len(dict_personal['ingeneru_vukonavci']) < 2:
            while len(dict_personal['ingeneru_vukonavci']) < 3:
                dict_personal['ingeneru_vukonavci'].append(" ")

# відкриття файлу з нормами замірів
with open('Data\\json\\normu_zamiriv.json', 'r', encoding='utf-8') as normu_zamiriv:
    dict_normu_zamiriv = json.load(normu_zamiriv)

# відкриття файлу з шляхами до файлів шаблонів docx формату
with open('Data\\json\\path_to_file.json', 'r', encoding='utf-8') as file_to_f:
    dict_file_to_file = json.load(file_to_f)

# """ ВІДПОВІДЬ ПРО ВІДПОВІДНІСТЬ ПУНКТУ """
# def slice_string(str_, len_str):  # залишає вказану к-ть знаків
#     return str_[:int(len_str)].strip()  # вставляє сам вираз без пробілів по боках і не дозволяє його встановити


"створюється клас для налаштування випадаючого меню в SPINNER"


class SpinnerCustomSetting(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 12  # Set custom font size
        self.background_color = .0, .722, .624, 1

        # print(self.size) # 100*48  - по замовчуванню

        self.color = "#00FFFF"
        self.halign = "center"
        self.valign = "center"


class SpinnerCustomSetting_narrow_s_font_10(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 11  # Set custom font size
        self.background_color = .0, .722, .624, 1

        # print(self.size) # 100*48
        self.text_size = 35, None
        self.color = "#00FFFF"
        self.halign = "center"
        self.valign = "center"

    pass


""" ГЛОБАЛЬНІ ЗМІННІ"""
global_kategoria_ktz = ""
luft_kerma = ""
txt_dlia_zapusiv = ""


class HelpingFun():
    def __init__(self):
        """ ВІДПОВІДЬ ПРО ВІДПОВІДНІСТЬ ПУНКТУ """
        self.kategorii = ['-', 'M1', 'M2', 'M3', 'N1', 'N2', 'N3', 'O1', 'O2', 'O3', 'O4']  #
        self.tak_ni_ns = ['ТАК', 'НІ', 'НС']  #
        self.nahul_tumanuh_far = ["-", '2%', '4%']
        self.pochatkovui_nahul_blugnih_far = "1.25"
        self.typ_error = ['НЕЗНАЧНІ', 'ЗНАЧНІ', 'НЕБЕЗПЕЧНІ']
        self.indukator_shun = ['НАЯВНИЙ', 'ВІДСУТНІЙ']
        self.info_naiavnisti = ['НАЯВНІ(Й)', 'ВІДСУТНІ(Й)', 'НС']
        self.vusnovok_otk = ['ВІДПОВІДАЄ', 'НЕ ВІДПОВІДАЄ']

    @staticmethod
    def slice_string(str_, len_str):  # залишає вказану к-ть знаків
        return str_[:int(len_str)].strip()  # вставляє сам вираз без пробілів по боках і не дозволяє його встановити

    @staticmethod
    def show_window_popup(vumoga_punctu):
        show = MesageWindowPopup()
        show.ids.lbl_popup.font_size = 14
        show.ids.lbl_popup.text = vumoga_punctu

        popup_obj = Popup(title="ПОВНИЙ ТЕКСТ ВИМОГИ",
                          content=show,
                          # content=Label(text= vumoga_punctu , text_size=(self.width, None),)
                          auto_dismiss=False,
                          # By default, any click outside the popup will dismiss/close it. If you don't want that, you can set
                          size_hint=(None, None),
                          size=(400, 400)
                          )

        popup_obj.open()  # відкриває виринаюче вікно

        """ В Обєкті виринаюче вікно (popup_obj), знаходять кнопку під id == btn_popup, і присвоюєтсья дія popup_obj.dismiss, 
        що закриває це вікною
        """
        #  Закриває виринаюче вікно при натиску кнопки
        show.ids.btn_popup.on_press = popup_obj.dismiss


    def boxlayout_btn_textinput(self, btn_id, btn_size_hint, btn_text_size, btn_text, btn_halign, btn_on_press,
                                t_input_id, t_input_size_hint, t_input_text):
        box_lt = BoxLayout()

        btn = Button(id=btn_id,
                     size_hint=btn_size_hint,
                     text_size=btn_text_size,
                     text=btn_text,
                     halign=btn_halign,
                     on_press=btn_on_press
                     )
        t_input = TextInput(id=t_input_id, size_hint=btn_size_hint, text=t_input_text)

        box_lt.add_widget(btn)
        box_lt.add_widget(t_input)

        return box_lt

    def boxlayout_btn_spiner(self, btn_id, btn_size_hint, btn_text_size, btn_text, btn_halign, btn_on_press,
                             spn_id, spn_size_hint, spn_text, spn_values, spn_background_color):
        box_lt = BoxLayout()

        btn = Button(id=btn_id,
                     size_hint=btn_size_hint,
                     text_size=btn_text_size,
                     text=btn_text,
                     halign=btn_halign,
                     on_press=btn_on_press
                     )

        spinner = Spinner(id=spn_id,
                          size_hint=spn_size_hint,
                          text=spn_text,
                          value=spn_values,
                          background_color=spn_background_color
                          )

        box_lt.add_widget(btn)
        box_lt.add_widget(spinner)

        return box_lt


# конструкція в screen.kv файлі
class MesageWindowPopup(Screen):
    pass


# конструкція в screen.kv файлі
class ZamitkuWindowPopup(Screen):
    pass


#
# def show_window_popup(vumoga_punctu):
#     # створюється вікно обєкту
#     show = MesageWindowPopup()
#     show.ids.lbl_popup.font_size = 14
#     show.ids.lbl_popup.text = vumoga_punctu
#
#     popup_obj = Popup(title="ПОВНИЙ ТЕКСТ ВИМОГИ",
#                       content=show,
#                       # content=Label(text= vumoga_punctu , text_size=(self.width, None),)
#                       auto_dismiss=False,
#                       # By default, any click outside the popup will dismiss/close it. If you don't want that, you can set
#                       size_hint=(None, None),
#                       size=(400, 400)
#                       )
#
#     popup_obj.open()  # відкриває виринаюче вікно
#
#     """ В Обєкті виринаюче вікно (popup_obj), знаходять кнопку під id == btn_popup, і присвоюєтсья дія popup_obj.dismiss,
#     що закриває це вікною
#     """
#     #  Закриває виринаюче вікно при натиску кнопки
#     show.ids.btn_popup.on_press = popup_obj.dismiss


class MainScreens(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


class First_page_screen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #
    def selected_kategory(self, spn_text):

        global luft_kerma, global_kategoria_ktz
        try:
            global_kategoria_ktz = spn_text

            print(" global_kategoria_ktz", global_kategoria_ktz)
            "створюється доступ до коріного віджета додатку"
            app = App.get_running_app()
            root = app.root
            # print(root.get_screen('four_page_screen').ids)

            # заповнення комірки люфт в рульовому керуванні
            root.root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_kerm_luft.text = Thrid_page(
            ).luft_kolis(global_kategoria_ktz)


        except Exception:
            pass

    "функція, що дозволяє рухати екран дотиками"
    # def on_touch_move(self, touch):
    #     if touch.dx > 20:  # Swipe right
    #         self.manager.transition.direction = 'right'
    #         self.manager.current = 'second_page_screen'
    #     elif touch.dx < -20:  # Swipe left
    #         self.manager.transition.direction = 'left'
    #         self.manager.current = "thrid_page_screen"
    #     return super(First_page_screen, self).on_touch_move(touch)


class Second_page_screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


class Thrid_page_screen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


class Four_page_screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


class Fifth_page_screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


class Nalashtuvania_screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


class Dlia_zamitok():

    def txt_dlia_zapusiv(self):
        show = ZamitkuWindowPopup()

        # присвоєння даних з глобальнoї змінної (txt_dlia_zapusiv) до поля введення тексту
        show.ids.ti_popup_zamitku.text = txt_dlia_zapusiv

        # СТВОРЕННЯ ДІАЛОГОВОГО ВІКНА
        popup_obj = Popup(title="ДЛЯ ЗАМІТОК",
                          content=show,
                          auto_dismiss=False,
                          # By default, any click outside the popup will dismiss/close it. If you don't want that, you can set
                          size_hint=(None, None),
                          size=(400, 400)
                          )

        def on_dismiss():
            global txt_dlia_zapusiv  # ЗВЕРНЕННЯ ДОГЛОБАЛНОЇ ЗМІННОЇ
            txt_dlia_zapusiv = show.ids.ti_popup_zamitku.text
            print("text_in_TextInput =", txt_dlia_zapusiv)
            popup_obj.dismiss()

        popup_obj.open()  # відкриває виринаюче вікно

        #  закриває ДІАЛОГОВЕ ВІКНО
        show.ids.btn_popup_zamitku.on_press = on_dismiss


class Print_btn():
    def __init__(self):
        self.app = App.get_running_app()
        self.root = self.app.root

    def druk_protokolu_otk(self):
        global txt_dlia_zapusiv

        dict_data = self.zbir_danuh_dlia_otokolu_otk()
        path_to_file_tmp = dict_file_to_file['path_to_file_tmp'],
        vin_code = dict_data['ti_vin_code'],
        path_to_folder_save = dict_file_to_file['path_to_folder_save']

        # робить заміну у файлі шаблоні та зберігає вже замінений файл
        WordReplace(dict_data, path_to_file_tmp, vin_code, path_to_folder_save
                    ).replace_data_in_file_and_save_it()

        # СТИРАННЯ ДАНИХ З ПОЛЯ ЗАМІТКИ
        self.root.get_screen('first_page_screen').ids.first_page.ids.ti_vin_code.text = ''
        self.root.get_screen('first_page_screen').ids.first_page.ids.ti_derj_nomer.text = ''
        self.root.get_screen('first_page_screen').ids.first_page.ids.ti_seria_tehpasportu.text = ''
        txt_dlia_zapusiv = ""

    def zbir_danuh_dlia_otokolu_otk(self):
        # app = App.get_running_app()
        # root = app.root
        root = self.root
        "ДАНІ ЩО ВНЕСЕНІ В ПРОТОКОЛ ВИПРОБУВАНЬ ОТК"

        dict_data_protocol = {
            # ІНФО ПРО ЛАБОРАТОРІЮ"
            'lv_name': root.get_screen('nalashtuvania_screen').ids.nalashtuvania_page.ids.lv_name.text,
            'lv_adressa': root.get_screen('nalashtuvania_screen').ids.nalashtuvania_page.ids.lv_adressa.text,
            'lv_atestat': root.get_screen('nalashtuvania_screen').ids.nalashtuvania_page.ids.lv_atestat.text,
            'adressa_vuprobuvan': root.get_screen(
                'nalashtuvania_screen').ids.nalashtuvania_page.ids.adressa_vuprobuvan.text,
            'nomer_v_gsc': root.get_screen('nalashtuvania_screen').ids.nalashtuvania_page.ids.nomer_v_gsc.text,
            'nomer_dilnuci': root.get_screen('nalashtuvania_screen').ids.nalashtuvania_page.ids.nomer_dilnuci.text,

            # 1 ПЕРШИЙ ЕКРАН"
            'ti_nomer_protocolu': root.get_screen('first_page_screen').ids.first_page.ids.ti_nomer_protocolu.text,
            'ti_data_test': root.get_screen('first_page_screen').ids.first_page.ids.ti_data_test.text,
            'ti_vin_code': root.get_screen('first_page_screen').ids.first_page.ids.ti_vin_code.text,
            'ti_derj_nomer': root.get_screen('first_page_screen').ids.first_page.ids.ti_derj_nomer.text,
            'ti_seria_tehpasportu': root.get_screen('first_page_screen').ids.first_page.ids.ti_seria_tehpasportu.text,
            'sp_kategoria': root.get_screen('first_page_screen').ids.first_page.ids.sp_kategoria.text,
            'ti_vantajnist': root.get_screen('first_page_screen').ids.first_page.ids.ti_vantajnist.text,
            'sp_identif': root.get_screen('first_page_screen').ids.first_page.ids.sp_identif.text,

            # ОСОБЛИВОСТІ КОНСТРУКЦІЇ - будуть оновлятися  в replace_data_in_file_and_save_it - class WordReplace:"

            # 2- ДРУГИЙ ЕКРАН"
            'sp_zamku_dverey': root.get_screen('second_page_screen').ids.second_page.ids.sp_zamku_dverey.text,
            'sp_remeni_bezpeku': root.get_screen('second_page_screen').ids.second_page.ids.sp_remeni_bezpeku.text,
            'sp_pidgolivnuku': root.get_screen('second_page_screen').ids.second_page.ids.sp_pidgolivnuku.text,
            'sp_ogliadovist': root.get_screen('second_page_screen').ids.second_page.ids.sp_ogliadovist.text,
            'sp_scolu_trihchinu': root.get_screen('second_page_screen').ids.second_page.ids.sp_scolu_trihchinu.text,
            'sp_markuv_scla': root.get_screen('second_page_screen').ids.second_page.ids.sp_markuv_scla.text,
            'ti_svitlo_vitrove': root.get_screen('second_page_screen').ids.second_page.ids.ti_svitlo_vitrove.text,
            'ti_svitlo_bokove': root.get_screen('second_page_screen').ids.second_page.ids.ti_svitlo_bokove.text,
            'ti_svitlo_zadne': root.get_screen('second_page_screen').ids.second_page.ids.ti_svitlo_zadne.text,
            'sp_osi_pidviska': root.get_screen('second_page_screen').ids.second_page.ids.sp_osi_pidviska.text,
            'sp_tusk_v_shinach': root.get_screen('second_page_screen').ids.second_page.ids.sp_tusk_v_shinach.text,
            'sp_indukator_shin': root.get_screen('second_page_screen').ids.second_page.ids.sp_indukator_shin.text,
            'ti_vusota_protector_shin': root.get_screen(
                'second_page_screen').ids.second_page.ids.ti_vusota_protector_shin.text,
            'sp_spidometr': root.get_screen('second_page_screen').ids.second_page.ids.sp_spidometr.text,
            'sp_tahograf': root.get_screen('second_page_screen').ids.second_page.ids.sp_tahograf.text,
            'sp_obmeg_hvudkosti': root.get_screen('second_page_screen').ids.second_page.ids.sp_obmeg_hvudkosti.text,
            'sp_shasi': root.get_screen('second_page_screen').ids.second_page.ids.sp_shasi.text,
            'sp_kripl_van_platform': root.get_screen(
                'second_page_screen').ids.second_page.ids.sp_kripl_van_platform.text,
            'sp_pidtikanua_ridunu': root.get_screen('second_page_screen').ids.second_page.ids.sp_pidtikanua_ridunu.text,

            # 3- ТРЕТІЙ ЕКРАН"
            # ДВИГУН ТА ЙОГО СИСТЕМИ
            'sp_engine_paluvo': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_engine_paluvo.text,
            'sp_engine_givlenia': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_engine_givlenia.text,
            'ti_noise': root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_noise.text,
            'sp_naiavnist_obd': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_naiavnist_obd.text,
            'sp_engine_obd': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_engine_obd.text,

            # ГАЛЬМІВНІ СИСИТЕМИ
            'sp_rgs': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_rgs.text,
            'sp_rgs_tech_stan': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_rgs_tech_stan.text,
            'sp_sgs': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_sgs.text,
            'sp_sgs_tech_stan': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_sgs_tech_stan.text,
            'sp_zgs_pracezdatnist': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_zgs_pracezdatnist.text,

            # РУЛЬОВЕ КЕРУВАННЯ ТЕХНІЧНІ ВИМОГИ
            'sp_pidsuluvach': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_pidsuluvach.text,
            'sp_signal_electro_pidsul': root.get_screen(
                'thrid_page_screen').ids.thrid_page.ids.sp_signal_electro_pidsul.text,
            'ti_kerm_luft': root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_kerm_luft.text,
            'sp_riven_rob_ridunu': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_riven_rob_ridunu.text,
            'sp_rul_tech_stan': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_rul_tech_stan.text,

            # ВОГНІ СВІТЛОВІДБИВАЧІ ЕЛЕКТРООБЛАДНАННЯ
            'sp_kilkist_far': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_kilkist_far.text,
            'sp_nahul_blugnih_far': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_nahul_blugnih_far.text,
            'ti_nahul_blugnih_far': root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_nahul_blugnih_far.text,
            'ti_nEosvit_liva_fara': root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_nEosvit_liva_fara.text,
            'ti_nEosvit_prava_fara': root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_nEosvit_prava_fara.text,
            'ti_Osvit_liva_fara': root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_Osvit_liva_fara.text,
            'ti_Osvit_prava_fara': root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_Osvit_prava_fara.text,
            'ti_sula_svitla_dal_faru_left': root.get_screen(
                'thrid_page_screen').ids.thrid_page.ids.ti_sula_svitla_dal_faru_left.text,
            'ti_sula_svitla_dal_faru_right': root.get_screen(
                'thrid_page_screen').ids.thrid_page.ids.ti_sula_svitla_dal_faru_right.text,
            'ti_suma_sul_svitla_dalnih_far': root.get_screen(
                'thrid_page_screen').ids.thrid_page.ids.ti_suma_sul_svitla_dalnih_far.text,
            'sp_nahul_tumannuh_far': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_nahul_tumannuh_far.text,
            'ti_liva_tumanka': root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_liva_tumanka.text,
            'ti_prava_tumanka': root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_prava_tumanka.text,
            'sp_sula_svitla_inshih_pzs': root.get_screen(
                'thrid_page_screen').ids.thrid_page.ids.sp_sula_svitla_inshih_pzs.text,
            'ti_chastota_probluskiv_povorotiv': root.get_screen(
                'thrid_page_screen').ids.thrid_page.ids.ti_chastota_probluskiv_povorotiv.text,
            'sp_gabarutni_vogni': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_gabarutni_vogni.text,
            'sp_electroobladnania': root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_electroobladnania.text,

            # 4 - ЧЕТВЕРТИЙ ЕКРАН
            # ВИМОГИ ГБО
            'sp_gbo': root.get_screen('four_page_screen').ids.four_page.ids.sp_gbo.text,
            # ДОДАТКОВІ ВИМОГИ ДО АВТОБУСІВ
            'sp_dodatkovi_perevirku_avtobusiv': root.get_screen(
                'four_page_screen').ids.four_page.ids.sp_dodatkovi_perevirku_avtobusiv.text,
            # ДОДАТКОВІ ВИМОГИ ДО ШК. АВТОБУСІВ
            'sp_shkolnik': root.get_screen('four_page_screen').ids.four_page.ids.sp_shkolnik.text,

            # ДОДАТКОВІ ВИМОГИ ДО ТАКСІ
            'sp_dodatk_taxi': root.get_screen('four_page_screen').ids.four_page.ids.sp_dodatk_taxi.text,

            # ДОДАТКОВІ ВИМОГИ ДО НЕГАБАРИТНИХ ВАНТАЖІВ
            'sp_dodatk_negabarut': root.get_screen('four_page_screen').ids.four_page.ids.sp_dodatk_negabarut.text,

            #  ВИМОГИ ДО НЕБЕЗПЕЧНИХ ВАНТАЖІВ
            'sp_nebez0': root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez0.text,
            'sp_nebez1': root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez1.text,
            'sp_nebez2': root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez2.text,
            'sp_nebez3': root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez3.text,
            'sp_nebez4': root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez4.text,
            'sp_nebez5': root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez5.text,

            # ВИМОГИ ДО НАВЧАЛЬНИХ КТЗ
            'sp_uchbovui': root.get_screen('four_page_screen').ids.four_page.ids.sp_uchbovui.text,

            # 5- ПЯТИЙ ЕКРАН
            # інші вимоги
            'sp_inshi_vumogu':root.get_screen('fifth_page_screen').ids.fifth_page.ids.sp_inshi_vumogu.text,

            # перелік невідповідностей
            'ti_error_neznachni_1': root.get_screen('fifth_page_screen').ids.fifth_page.ids.ti_error_neznachni_1.text,
            'ti_error_neznachni_2': root.get_screen('fifth_page_screen').ids.fifth_page.ids.ti_error_neznachni_2.text,
            'ti_error_neznachni_3': root.get_screen('fifth_page_screen').ids.fifth_page.ids.ti_error_neznachni_3.text,
            'ti_error_znachni_1': root.get_screen('fifth_page_screen').ids.fifth_page.ids.ti_error_znachni_1.text,
            'ti_error_znachni_2': root.get_screen('fifth_page_screen').ids.fifth_page.ids.ti_error_znachni_2.text,
            'ti_error_znachni_3': root.get_screen('fifth_page_screen').ids.fifth_page.ids.ti_error_znachni_3.text,
            'ti_error_nebezpechni_1': root.get_screen(
                'fifth_page_screen').ids.fifth_page.ids.ti_error_nebezpechni_1.text,
            'ti_error_nebezpechni_2': root.get_screen(
                'fifth_page_screen').ids.fifth_page.ids.ti_error_nebezpechni_2.text,
            'ti_error_nebezpechni_3': root.get_screen(
                'fifth_page_screen').ids.fifth_page.ids.ti_error_nebezpechni_3.text,

            # висновок про відповдіність
            'sp_vusnovok_otk': root.get_screen('fifth_page_screen').ids.fifth_page.ids.sp_vusnovok_otk.text,

            # ДЛЯ ЗАПИСІВ
            'v_dlia_zapusiv': txt_dlia_zapusiv,

            # ПЕРСОНАЛ
            'sp_kerivnuk_dilnuci': root.get_screen('fifth_page_screen').ids.fifth_page.ids.sp_kerivnuk_dilnuci.text,
            'sp_first_enginner': root.get_screen('fifth_page_screen').ids.fifth_page.ids.sp_first_enginner.text,
            'sp_second_enginner': root.get_screen('fifth_page_screen').ids.fifth_page.ids.sp_second_enginner.text
        }
        # pprint(dict_data_protocol)
        return dict_data_protocol

        # "dict_data_protocol"
        # pprint( dict_data_protocol)


class MyApp(App):

    def build(self):
        Window.size = (720, 600)  # розміри вікна

        Builder.load_file("Data\\kv\\Screens.kv")

        Builder.load_file("Data\\kv\\First_page.kv")
        Builder.load_file("Data\\kv\\Second_page.kv")
        Builder.load_file("Data\\kv\\Thrid_page.kv")
        Builder.load_file("Data\\kv\\Four_page.kv")
        Builder.load_file("Data\\kv\\Fifth_page.kv")

        Builder.load_file("Data\\kv\\Nalashtuvania_page.kv")

        # First_page_screen().info()
        # Thrid_page_screen().luft_kerma()
        # global_kategoria_ktz  =First_page().ids.spinner_kategoria.text
        # print("global_kategoria_ktz",  global_kategoria_ktz)

        # arr_model = [First_page(), Second_page(), Thrid_page(), Four_page(), Fifth_page(), Nalashtuvania_page()]
        #
        # d= {}
        # for _p in arr_model:
        #     for _ in _p.ids:
        #         d[f"{_}"] = None
        #
        # pprint(d)
        # print(d)

        self.title = f"ПЕРВИННИЙ ПРОТОКОЛ УКРВЕСТАВТО ДІЛЬНИЦЯ № {dict_info_about_dilnuci_lv['nomer_dilnuci']}"  # назва вікна
        self.icon = 'logo_uwa.jpg'

        # запускає клас
        return MainScreens(transition=SlideTransition())

    """ ОСОБЛИВОСТІ КОНСТРУКЦІЇ """

    # "['first_page_screen', 'second_page_screen', 'thrid_page_screen', 'four_page_screen', 'fifth_page_screen', 'nalashtuvania_screen']"

    def tb_ditu(self, id_tg_botton):
        """  self.root використовується для доступу до кореневого віджета додатка, яким у нашому випадку є MainScreens.
         Кореневий віджет встановлюється методом build класу App, і він містить усі інші віджети та екрани додатка. """
        # print(MainScreens().screen_names)
        if id_tg_botton.state == 'normal':
            self.root.get_screen('four_page_screen').ids.four_page.ids.dod_vumogu_ditu.disabled = True
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_shkolnik.text = HelpingFun().tak_ni_ns[2]

        if id_tg_botton.state == 'down':
            self.root.get_screen('four_page_screen').ids.four_page.ids.dod_vumogu_ditu.disabled = False
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_shkolnik.text = HelpingFun().tak_ni_ns[0]

    def tb_taxi(self, id_tg_botton):

        # print(MainScreens().screen_names)
        if id_tg_botton.state == 'normal':
            self.root.get_screen('four_page_screen').ids.four_page.ids.dod_vumogu_taxi.disabled = True
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_dodatk_taxi.text = HelpingFun().tak_ni_ns[2]

        if id_tg_botton.state == 'down':
            self.root.get_screen('four_page_screen').ids.four_page.ids.dod_vumogu_taxi.disabled = False
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_dodatk_taxi.text = HelpingFun().tak_ni_ns[0]

    def tb_negabarut(self, id_tg_botton):

        if id_tg_botton.state == 'normal':
            self.root.get_screen('four_page_screen').ids.four_page.ids.dod_vumogu_negabarut.disabled = True
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_dodatk_negabarut.text = \
                HelpingFun().tak_ni_ns[2]

        if id_tg_botton.state == 'down':
            self.root.get_screen('four_page_screen').ids.four_page.ids.dod_vumogu_negabarut.disabled = False
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_dodatk_negabarut.text = \
                HelpingFun().tak_ni_ns[0]

    def tb_navchalnuy(self, id_tg_botton):

        if id_tg_botton.state == 'normal':
            self.root.get_screen('four_page_screen').ids.four_page.ids.dod_vumogu_navchalni_ktz.disabled = True
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_uchbovui.text = HelpingFun().tak_ni_ns[2]

        if id_tg_botton.state == 'down':
            self.root.get_screen('four_page_screen').ids.four_page.ids.dod_vumogu_navchalni_ktz.disabled = False
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_uchbovui.text = HelpingFun().tak_ni_ns[0]

    def tb_tumanka(self, id_tg_botton):

        if id_tg_botton.state == 'normal':
            # pprint(MainScreens().get_screen('thrid_page_screen').ids)
            self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.id_tumanni_faru.disabled = True
            self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_nahul_tumannuh_far.text = \
                HelpingFun().nahul_tumanuh_far[0]
            self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_liva_tumanka.text = "-"
            self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_prava_tumanka.text = "-"

        if id_tg_botton.state == 'down':
            self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.id_tumanni_faru.disabled = False
            self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.sp_nahul_tumannuh_far.text = \
                HelpingFun().nahul_tumanuh_far[0]
            self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_liva_tumanka.text = str(rnd.randrange(
                dict_normu_zamiriv["tumanni_faru"][0], dict_normu_zamiriv["tumanni_faru"][1],
                dict_normu_zamiriv["tumanni_faru"][2]
            )
            )
            self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_prava_tumanka.text = str(rnd.randrange(
                dict_normu_zamiriv["tumanni_faru"][0], dict_normu_zamiriv["tumanni_faru"][1],
                dict_normu_zamiriv["tumanni_faru"][2]
            )
            )

    def tb_nebezpechiy(self, id_tg_botton):

        if id_tg_botton.state == 'normal':
            self.root.get_screen('four_page_screen').ids.four_page.ids.id_nebezpechniy_row_1.disabled = True
            self.root.get_screen('four_page_screen').ids.four_page.ids.id_nebezpechniy_row_2.disabled = True
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez0.text = HelpingFun().tak_ni_ns[2]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez1.text = HelpingFun().tak_ni_ns[2]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez2.text = HelpingFun().tak_ni_ns[2]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez3.text = HelpingFun().tak_ni_ns[2]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez4.text = HelpingFun().tak_ni_ns[2]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez5.text = HelpingFun().tak_ni_ns[2]

        if id_tg_botton.state == 'down':
            self.root.get_screen('four_page_screen').ids.four_page.ids.id_nebezpechniy_row_1.disabled = False
            self.root.get_screen('four_page_screen').ids.four_page.ids.id_nebezpechniy_row_2.disabled = False
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez0.text = HelpingFun().tak_ni_ns[0]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez1.text = HelpingFun().tak_ni_ns[0]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez2.text = HelpingFun().tak_ni_ns[0]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez3.text = HelpingFun().tak_ni_ns[0]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez4.text = HelpingFun().tak_ni_ns[0]
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_nebez5.text = HelpingFun().tak_ni_ns[0]

    def tb_gbo(self, id_tg_botton):

        if id_tg_botton.state == 'normal':
            self.root.get_screen('four_page_screen').ids.four_page.ids.id_gbo.disabled = True
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_gbo.text = HelpingFun().tak_ni_ns[2]

        if id_tg_botton.state == 'down':
            self.root.get_screen('four_page_screen').ids.four_page.ids.id_gbo.disabled = False
            self.root.get_screen('four_page_screen').ids.four_page.ids.sp_gbo.text = HelpingFun().tak_ni_ns[0]

    "Налаштування вигляду вимог для різних категорій"

    def bus_add_vumogu(self, global_kategoria_ktz):

        if global_kategoria_ktz == "M2" or global_kategoria_ktz == "M3":

            self.root.get_screen('four_page_screen').ids.four_page.ids.bl_dod_vunogu_do_avtobusiv.disabled = False
            self.root.get_screen('four_page_screen'
                                 ).ids.four_page.ids.sp_dodatkovi_perevirku_avtobusiv.text = HelpingFun().tak_ni_ns[0]

        else:
            self.root.get_screen('four_page_screen').ids.four_page.ids.bl_dod_vunogu_do_avtobusiv.disabled = True
            self.root.get_screen('four_page_screen'
                                 ).ids.four_page.ids.sp_dodatkovi_perevirku_avtobusiv.text = HelpingFun().tak_ni_ns[2]

    def set_screens_for_kategoria_ktz(self, kategoriz_ktz):

        # ---------------- заповнення комірки висота протектора----------
        self.root.get_screen("second_page_screen").ids.second_page.ids.ti_vusota_protector_shin.text = Second_page(
        ).vusota_protectora_shun(kategoriz_ktz)

        if kategoriz_ktz in ["M1", "M2", "M3", "N1", "N2", "N3"]:
            # заповнення комірки люфт в рульовому керуванні
            self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_kerm_luft.text = Thrid_page(
            ).luft_kolis(kategoriz_ktz)

            "змінюємо властивості віджетів на сторінках"
            # ---------замки дверей ремені безпеки підголівники---------
            self.root.get_screen("second_page_screen").ids.second_page.ids.m_n_1.disabled = False
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_zamku_dverey.text = \
                HelpingFun().tak_ni_ns[0]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_remeni_bezpeku.text = \
                HelpingFun().tak_ni_ns[0]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_pidgolivnuku.text = \
                HelpingFun().tak_ni_ns[0]

            # --------- поле огляду світлопропускання скла---------
            self.root.get_screen("second_page_screen").ids.second_page.ids.m_n_2.disabled = False

            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_ogliadovist.text = HelpingFun().tak_ni_ns[
                0]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_scolu_trihchinu.text = \
                HelpingFun().info_naiavnisti[1]

            self.root.get_screen(
                "second_page_screen").ids.second_page.ids.ti_svitlo_vitrove.text = Second_page().svitlopropuskania_vitrove()
            self.root.get_screen(
                "second_page_screen").ids.second_page.ids.ti_svitlo_bokove.text = Second_page().svitlopropuskania_bokove_zadnie()
            self.root.get_screen("second_page_screen").ids.second_page.ids.ti_svitlo_zadne.text = "-"

            # ----------------спідометр- тахогроаф обмеження швидкості-------
            self.root.get_screen("second_page_screen").ids.second_page.ids.m_n_3.disabled = False
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_spidometr.text = HelpingFun(
            ).tak_ni_ns[0]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_tahograf.text = HelpingFun(
            ).tak_ni_ns[0]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_obmeg_hvudkosti.text = HelpingFun(
            ).tak_ni_ns[2]

            # системи двигуна
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.engine_and_system.disabled = False
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_engine_paluvo.text = \
                dict_f_vumogu_otk['engine_paluvo'][0]

            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_engine_givlenia.text = \
                dict_f_vumogu_otk['engine_givlenia'][0]

            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_noise.text = "---"
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_naiavnist_obd.text = \
                HelpingFun().info_naiavnisti[0]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_engine_obd.text = \
                dict_f_vumogu_otk['perevirka_obd_error'][1]

            # рульове керування
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ruluve_keruvania.disabled = False
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_pidsuluvach.text = HelpingFun().tak_ni_ns[0]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_signal_electro_pidsul.text = \
                HelpingFun().tak_ni_ns[0]
            # self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_kerm_luft.text = Thrid_page().luft_kolis(
            #     global_kategoria_ktz)
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_riven_rob_ridunu.text = \
                HelpingFun().tak_ni_ns[0]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_rul_tech_stan.text = HelpingFun(
            ).tak_ni_ns[0]

            # ближнє та дальне світло
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.bl_faru.disabled = False
            # кут нахилу фар ближнього світла

            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_nahul_blugnih_far.text = HelpingFun(
            ).pochatkovui_nahul_blugnih_far
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_nahul_blugnih_far.text = HelpingFun(
            ).tak_ni_ns[0]
            # -------

            self.root.get_screen(
                "thrid_page_screen").ids.thrid_page.ids.ti_nEosvit_liva_fara.text = Thrid_page().liva_fara_NEosvitlena
            self.root.get_screen(
                "thrid_page_screen").ids.thrid_page.ids.ti_nEosvit_prava_fara.text = Thrid_page().prava_fara_NEosvitlena
            self.root.get_screen(
                "thrid_page_screen").ids.thrid_page.ids.ti_Osvit_liva_fara.text = Thrid_page().liva_fara_osvitlena
            self.root.get_screen(
                "thrid_page_screen").ids.thrid_page.ids.ti_Osvit_prava_fara.text = Thrid_page().prava_fara_osvitlena
            self.root.get_screen(
                "thrid_page_screen").ids.thrid_page.ids.ti_sula_svitla_dal_faru_left.text = Thrid_page().liva_fara_dalna
            self.root.get_screen(
                "thrid_page_screen").ids.thrid_page.ids.ti_sula_svitla_dal_faru_right.text = Thrid_page().prava_fara_dalna
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_suma_sul_svitla_dalnih_far.text = str(
                Thrid_page().liva_plus_prava_fara_dalna)

        if kategoriz_ktz in ["O1", "O2", "O3", "O4"]:
            # заповнення комірки люфт в рульовому керуванні
            # self.root.get_screen('thrid_page_screen').ids.thrid_page.ids.ti_kerm_luft.text = HelpingFun(
            # ).tak_ni_ns[2]

            "змінюємо властивості віджетів на сторінках"
            # ---------замки та ремені безпеки підголівники---------
            self.root.get_screen("second_page_screen").ids.second_page.ids.m_n_1.disabled = True
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_zamku_dverey.text = \
                HelpingFun().tak_ni_ns[2]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_remeni_bezpeku.text = \
                HelpingFun().tak_ni_ns[2]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_pidgolivnuku.text = \
                HelpingFun().tak_ni_ns[2]

            # ---------------світлопропускання скла-----------
            self.root.get_screen("second_page_screen").ids.second_page.ids.m_n_2.disabled = True
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_ogliadovist.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_scolu_trihchinu.text = HelpingFun(
            ).info_naiavnisti[2]

            self.root.get_screen("second_page_screen").ids.second_page.ids.m_n_2.disabled = True

            self.root.get_screen("second_page_screen").ids.second_page.ids.ti_svitlo_vitrove.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("second_page_screen").ids.second_page.ids.ti_svitlo_bokove.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("second_page_screen").ids.second_page.ids.ti_svitlo_zadne.text = HelpingFun(
            ).tak_ni_ns[2]

            # ----------------спідометр- тахогроаф обмеження швитдкості-------
            self.root.get_screen("second_page_screen").ids.second_page.ids.m_n_3.disabled = True
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_spidometr.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_tahograf.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("second_page_screen").ids.second_page.ids.sp_obmeg_hvudkosti.text = HelpingFun(
            ).tak_ni_ns[2]

            # системи двигуна
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.engine_and_system.disabled = True
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_engine_paluvo.text = HelpingFun(
            ).tak_ni_ns[2]

            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_engine_givlenia.text = HelpingFun(
            ).tak_ni_ns[2]

            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_noise.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_naiavnist_obd.text = HelpingFun(
            ).info_naiavnisti[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_engine_obd.text = \
                dict_f_vumogu_otk['perevirka_obd_error'][2]

            # рульове керування
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ruluve_keruvania.disabled = True
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_pidsuluvach.text = HelpingFun().tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_signal_electro_pidsul.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_kerm_luft.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_riven_rob_ridunu.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_rul_tech_stan.text = HelpingFun(
            ).tak_ni_ns[2]

            # ближнє та дальне світло
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.bl_faru.disabled = True
            # кут нахилу фар ближнього світла
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_nahul_blugnih_far.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.sp_nahul_blugnih_far.text = HelpingFun(
            ).tak_ni_ns[2]
            # -------
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_nEosvit_liva_fara.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_nEosvit_prava_fara.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_Osvit_liva_fara.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_Osvit_prava_fara.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_sula_svitla_dal_faru_left.text = HelpingFun(
            ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_sula_svitla_dal_faru_right.text = \
                HelpingFun(
                ).tak_ni_ns[2]
            self.root.get_screen("thrid_page_screen").ids.thrid_page.ids.ti_suma_sul_svitla_dalnih_far.text = \
                HelpingFun(
                ).tak_ni_ns[2]

            pass
        pass


#     --------------------

if __name__ == '__main__':

    '# має допомгти вирішити рекурсію'
    if hasattr(sys, '_MEIPASS'):
        os.environ['KIVY_NO_CONSOLELOG'] = '1'

    # або

    if sys.__stdout__ is None or sys.__stderr__ is None:
        os.environ['KIVY_NO_CONSOLELOG'] = '1'

    MyApp().run()
