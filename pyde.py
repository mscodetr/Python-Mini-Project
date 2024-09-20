import kivy
import sys
import io
import subprocess
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.popup import Popup
from kivy.uix.button import Button


# Renk paletini belirleyelim
dark_theme = {
    "bg_color": (0.15, 0.15, 0.15, 1),
    "fg_color": (1, 1, 1, 1),
    "button_color": (0.3, 0.3, 0.3, 1),
    "button_fg": (1, 1, 1, 1),
    "terminal_bg": (0, 0, 0, 1),
    "terminal_fg": (0.8, 0.8, 0.8, 1),
}

class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super(EditorScreen, self).__init__(**kwargs)
        self.build()

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Yatay layout, satır numaraları ve kod editörü için
        editor_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Satır numarası alanı
        self.line_numbers = TextInput(
            text='',
            size_hint=(None, 1),
            width=50,
            readonly=True,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )

        # Kod editörü
        self.code_editor = TextInput(
            hint_text="Write your Python code here...",
            size_hint=(1, 1),
            multiline=True,
            font_size=16,
            background_color=dark_theme['bg_color'],
            foreground_color=dark_theme['fg_color']
        )

        # Kod editörü her değiştiğinde satır numaralarını güncelle
        self.code_editor.bind(text=self.update_line_numbers)

        editor_layout.add_widget(self.line_numbers)
        editor_layout.add_widget(self.code_editor)

        # Terminal/Konsol
        self.terminal_output = TextInput(
            text="Terminal output will appear here...",
            size_hint=(1, 0.25),
            readonly=True,
            font_size=14,
            background_color=dark_theme['terminal_bg'],
            foreground_color=dark_theme['terminal_fg']
        )

        # Pip yükleme alanı
        self.pip_input = TextInput(
            hint_text="Enter package name to install...",
            size_hint=(1, 0.1),
            font_size=14,
            background_color=dark_theme['bg_color'],
            foreground_color=dark_theme['fg_color']
        )

        pip_button = Button(
            text="Install Package",
            size_hint=(1, 0.1),
            background_color=dark_theme['button_color'],
            color=dark_theme['button_fg']
        )
        pip_button.bind(on_press=self.install_package)

        # Butonlar için yatay layout
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)

        run_button = Button(
            text="Run",
            size_hint=(0.2, 1),
            background_color=dark_theme['button_color'],
            color=dark_theme['button_fg']
        )
        run_button.bind(on_press=self.run_code)

        open_button = Button(
            text="Open",
            size_hint=(0.2, 1),
            background_color=dark_theme['button_color'],
            color=dark_theme['button_fg']
        )
        open_button.bind(on_press=self.open_file)

        save_button = Button(
            text="Save",
            size_hint=(0.2, 1),
            background_color=dark_theme['button_color'],
            color=dark_theme['button_fg']
        )
        save_button.bind(on_press=self.save_file)

        settings_button = Button(
            text="Settings",
            size_hint=(0.2, 1),
            background_color=dark_theme['button_color'],
            color=dark_theme['button_fg']
        )
        settings_button.bind(on_press=self.open_settings)

        button_layout.add_widget(open_button)
        button_layout.add_widget(save_button)
        button_layout.add_widget(run_button)
        button_layout.add_widget(settings_button)

        layout.add_widget(editor_layout)  # Yatay layoutu ekle
        layout.add_widget(self.terminal_output)
        layout.add_widget(self.pip_input)
        layout.add_widget(pip_button)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def update_line_numbers(self, instance, value):
        line_count = len(value.splitlines())
        self.line_numbers.text = '\n'.join(str(i) for i in range(1, line_count + 1))

    def install_package(self, instance):
        package_name = self.pip_input.text.strip()
        if package_name:
            try:
                result = subprocess.run([sys.executable, "-m", "pip", "install", package_name],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)
                output = result.stdout + "\n" + result.stderr
                self.terminal_output.text = output if output else "Package installed successfully."
            except Exception as e:
                self.terminal_output.text = f"Error: {str(e)}"
        else:
            self.terminal_output.text = "Please enter a package name."

    def run_code(self, instance):
        code = self.code_editor.text

        old_stdout = sys.stdout
        sys.stdout = new_stdout = io.StringIO()

        try:
            exec(code)
            output = new_stdout.getvalue()
            self.terminal_output.text = output if output else "Code ran successfully."
        except Exception as e:
            self.terminal_output.text = f"Error: {str(e)}"
        finally:
            sys.stdout = old_stdout

    def open_file(self, instance):
        filechooser = FileChooserIconView()
        popup = Popup(title="Open File", content=filechooser, size_hint=(0.9, 0.9))
        popup.open()

        filechooser.bind(on_submit=lambda x, selection, y: self.load_file(selection, popup))

    def load_file(self, selection, popup):
        if selection:
            with open(selection[0], 'r') as f:
                self.code_editor.text = f.read()
            popup.dismiss()

    def save_file(self, instance):
        filechooser = FileChooserIconView()
        popup = Popup(title="Save File", content=filechooser, size_hint=(0.9, 0.9))
        popup.open()

        filechooser.bind(on_submit=lambda x, selection, y: self.save_to_file(selection, popup))

    def save_to_file(self, selection, popup):
        if selection:
            with open(selection[0], 'w') as f:
                f.write(self.code_editor.text)
            popup.dismiss()

    def open_settings(self, instance):
        self.manager.current = 'settings'


class SettingsScreen(Screen):
    def __init__(self, editor_screen, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.editor_screen = editor_screen
        self.build()

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        font_size_label = Label(text="Font Size", size_hint=(1, 0.1), color=dark_theme['fg_color'])
        self.font_size_slider = Slider(min=10, max=50, value=16, size_hint=(1, 0.1))
        self.font_size_slider.bind(value=self.change_font_size)

        back_button = Button(
            text="Back to Editor",
            size_hint=(1, 0.1),
            background_color=dark_theme['button_color'],
            color=dark_theme['button_fg']
        )
        back_button.bind(on_press=self.back_to_editor)

        layout.add_widget(font_size_label)
        layout.add_widget(self.font_size_slider)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def change_font_size(self, instance, value):
        self.editor_screen.code_editor.font_size = value

    def back_to_editor(self, instance):
        self.manager.current = 'editor'


class PythonIDEApp(App):
    def build(self):
        Window.clearcolor = dark_theme['bg_color']
        sm = ScreenManager()

        editor_screen = EditorScreen(name='editor')
        settings_screen = SettingsScreen(editor_screen=editor_screen, name='settings')

        sm.add_widget(editor_screen)
        sm.add_widget(settings_screen)

        return sm


if __name__ == "__main__":
    PythonIDEApp().run()
