
# налаштування розміру вікна ківі
from kivy.core.window import Window

Window.size = (720, 550)  # розміри вікна

from kivy.uix.widget import Widget
import os
from datetime import datetime
from kivy.uix.widget import ObjectProperty

import json
import random as rnd


from kivy.uix.textinput import TextInput
# Стенд проверки - рядки для замовлення де знаходиться стенд чи іншу інформацію


# ---------- ДЛЯ РОЗМІЩЕННЯ КЛАСІВ НА ЕКРАНАХ-----------

class Fifth_page(Widget):
    def open_file_with_nevidpovidnosti(self, path_to_file):
        os.startfile(path_to_file)


class Input_in_Text_nevidpovidnosti(Widget):
    pass