from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.properties import StringProperty
import os


class FileChooserWidget(BoxLayout):
    file_path = StringProperty('')

    def __init__(self, **kwargs):
        super(FileChooserWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Create a dropdown for selecting disks
        self.dropdown = DropDown()
        self.drives = self.get_drives()
        for drive in self.drives:
            btn = Button(text=drive, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.switch_drive(btn.text))
            self.dropdown.add_widget(btn)

        self.main_button = Button(text='Select Disk', size_hint=(1, 0.1))
        self.main_button.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.main_button, 'text', x))
        self.add_widget(self.main_button)

        # Create the file chooser
        self.file_chooser = FileChooserListView()
        self.add_widget(self.file_chooser)

        # Create a button to select a file
        self.select_button = Button(text='Select File', size_hint=(1, 0.1))
        self.select_button.bind(on_press=self.select_file)
        self.add_widget(self.select_button)

        # Create a label to display the selected file path
        self.file_label = Label(text=self.file_path)
        self.add_widget(self.file_label)

    def get_drives(self):
        # Function to get available drives (Windows example)
        if os.name == 'nt':
            import string
            return [f'{d}:' for d in string.ascii_uppercase if os.path.exists(f'{d}:\\')]
        else:
            # For other OS, listing root directories
            return ['/']

    def switch_drive(self, drive):
        self.file_chooser.path = drive
        self.file_chooser._update_files()

    def select_file(self, *args):
        if self.file_chooser.selection:
            self.file_path = self.file_chooser.selection[0]
            self.file_label.text = f'Selected file: {self.file_path}'


class FileChooserApp(App):
    def build(self):
        return FileChooserWidget()


if __name__ == '__main__':
    FileChooserApp().run()
