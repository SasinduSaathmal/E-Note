from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineRightIconListItem
from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty
from kivymd.icon_definitions import md_icons
from kivymd.uix.textfield import MDTextFieldRect
import os

Builder.load_file("filecreator.kv")


class TextEditor(MDFloatLayout):
    pass


class FileDialog(MDBoxLayout):
    pass


class FontChangeDialog(MDBoxLayout):
    pass


class ListItemWithCheckbox(OneLineRightIconListItem):
    text = StringProperty()


class ENoteApp(MDApp):
    def __init__(self, **kwargs):
        super(ENoteApp, self).__init__(**kwargs)
        self.texteditor = TextEditor()
        self.file_manager = None
        self.picked_file_path = None
        self.fdialog = FileDialog()
        self.filedialog = False
        self.font_change_dialog = FontChangeDialog()
        self.font_dialog = False
        self.fonts = None

    def build(self):
        # for name in md_icons.keys():
            # print(name)
        self.icon = "assets/icon.png"
        self.theme_cls.theme_style = "Dark"
        self.title = "E-Note"
        return self.texteditor

    def on_start(self):
        self.load_fonts()
        self.init_menu()

    def init_menu(self):
        self.menu_items = [
            {
                "viewclass": "ListItemWithCheckbox",
                "height": 60,
                "text": "Wrap Text"
            },
            {
                "text": "Change Font",
                "height": 60,
                "viewclass": "OneLineListItem",
                "on_release": self.open_font_dialog
            }
        ]

        self.menu = MDDropdownMenu(
            items=self.menu_items,
            ver_growth="down",
            hor_growth="right",
            position="auto",
            width_mult=3,
            max_height="120dp",
            elevation=3
        )

        self.fonts_menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    "height": 50,
                    "text": str(font),
                    "on_press": lambda x=str(font): self.on_fonts_menu_clicked(x)
                } for font in self.fonts
            ]

        self.fonts_menu = MDDropdownMenu(
                caller = self.font_change_dialog.ids.font,
                items = self.fonts_menu_items,
                width_mult = 4,
                ver_growth = "down",
                hor_growth = "right",
                position = "bottom",
                max_height = 300
            )

        self.font_size_menu_items = [
                {
                    "viewclass": "OneLineListItem", 
                    "height": 50,
                    "text": str(i),
                    "on_press": lambda x=str(i): self.on_font_size_change_menu_clicked(x)
                } for i in range(100)
            ]

        self.font_size_menu = MDDropdownMenu(
                caller = self.font_change_dialog.ids.font_size_input,
                items = self.font_size_menu_items,
                max_height = 200
            )

    def load_fonts(self):
        location = os.path.join("C:\\", "Windows", "Fonts")
        self.fonts = os.listdir(location)

    def filter_font_sizes(self, *args):
        input_font_size = self.font_change_dialog.ids.font_size_input.text
        def filter_font_size(font_size):
            if input_font_size in str(font_size):
                return True

        if not input_font_size == "":
            font_sizes = list(filter(filter_font_size, range(100)))
            updated_font_size_menu_items = [
                {
                    "viewclass": "OneLineListItem", 
                    "height": 50,
                    "text": str(i),
                    "on_press": lambda x=str(i): self.on_font_size_change_menu_clicked(x)
                } for i in font_sizes
            ]

            self.font_size_menu.items = updated_font_size_menu_items
            self.font_size_menu.dismiss()
            self.font_size_menu.open()

            self.font_size_menu.items = self.font_size_menu_items

    def filter_fonts(self):
        input_font = self.font_change_dialog.ids.font.text
        def filter_font(font):
            if input_font in font:
                return True

        if not input_font == "":
            new_fonts = list(filter(filter_font, self.fonts))
            updated_fonts_menu_items = [
                {
                    "viewclass": "OneLineListItem", 
                    "height": 50,
                    "text": str(font),
                    "on_press": lambda x=str(font): self.on_fonts_menu_clicked(x)
                } for font in new_fonts
            ]

            self.fonts_menu.items = updated_fonts_menu_items
            self.fonts_menu.dismiss()
            self.fonts_menu.open()

            self.fonts_menu.items = self.fonts_menu_items

    def save_file(self, path):
        print("Save")

        file_name = self.fdialog.ids.fname.text
        formatted_file_name = file_name if file_name.endswith(".txt") else file_name + ".txt"
        file_path = os.path.join(path, formatted_file_name)
        content = self.root.ids.text_box.text.splitlines()
        formatted_content = [content[i] + "\n" for i in range(len(content))]
        print(content)
        print(formatted_content)
        with open(file_path, "w") as file:
            file.writelines(formatted_content)

    def open_file(self, path):
        print("Open")
        with open(path, "r") as file:
            content = file.readlines()

        self.root.ids.text_box.text = "".join(content)

    def open_file_manager(self, method, *args):
        def save_file_callback(*args):
            self.filedialog.dismiss(force=True)
            self.file_manager.selector = "folder"
            self.file_manager.preview = preview
            path = os.path.expanduser("~")
            self.file_manager.show(path)

        preview = False
        self.method = method

        if not self.file_manager:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager,
                select_path=self.select_path,
                preview=preview,
            )

        if self.method == "open":
            self.file_manager.ext = [".txt"]
            self.file_manager.selector = "file"
            self.file_manager.preview = preview
            path = os.path.expanduser("~")
            self.file_manager.show(path)
        else:
            if not self.filedialog:
                self.filedialog = MDDialog(
                    title = "Enter the file name to save",
                    type = "custom",
                    content_cls = self.fdialog,
                    buttons = [
                        MDFlatButton(
                            text = "OK",
                            theme_text_color = "Primary",
                            on_release = save_file_callback
                            ),
                        MDFlatButton(
                            text = "CANCEL",
                            theme_text_color = "Secondary",
                            on_release = lambda x: self.dialogDismiss("file")
                            )
                        ]
                    )
            self.filedialog.open()

    def select_path(self, path):
        self.exit_manager()
        method = self.method
        if type(path) == str:
            self.picked_file_path = path
            self.save_file(path) if method == "save" else self.open_file(path)
        else:
            self.picked_file_path = ", ".join(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()
        self.file_manager = None

    def open_settings_menu(self, button):
        self.menu.caller = button
        self.menu.open()

    def on_text_wrap(self, checkbox, value):
        self.root.ids.text_box.do_wrap = value

    def open_font_dialog(self, *args):
        if not self.font_dialog:
            self.font_dialog = MDDialog(
                title = "Change Font Settings",
                type = "custom",
                content_cls = self.font_change_dialog,
                buttons = [
                    MDFlatButton(
                        text = "OK",
                        theme_text_color = "Primary",
                        on_release = self.change_font
                        ),
                    MDFlatButton(
                        text = "CANCEL",
                        theme_text_color = "Secondary",
                        on_release = lambda x: self.dialogDismiss("font")
                        )
                    ]
                )
        self.font_dialog.open()

    def change_font(self, *args):
        self.dialogDismiss("font")
        new_font = self.font_change_dialog.ids.font.text
        new_font_size = self.font_change_dialog.ids.font_size_input.text
        self.root.ids.text_box.font_name = new_font
        self.root.ids.text_box.font_size = float(new_font_size)

    def on_font_size_change_menu_clicked(self, font_size):
        self.font_size_menu.dismiss()
        self.font_change_dialog.ids.font_size_input.text = font_size

    def on_fonts_menu_clicked(self, font):
        self.fonts_menu.dismiss()
        self.font_change_dialog.ids.font.text = font

    def dialogDismiss(self, dialog):
        if dialog == "font":
            self.font_dialog.dismiss(force=True)
        elif dialog == "file":
            self.filedialog.dismiss(force=True)

if __name__ == "__main__":
    ENoteApp().run()

