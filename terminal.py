import sys  # Python sistem modülünü import ediyoruz
from kivy.app import App  # Kivy uygulama sınıfını import ediyoruz
from kivy.uix.screenmanager import ScreenManager, Screen  # Ekranları yönetmek için ScreenManager ve Screen sınıflarını import ediyoruz
from kivy.uix.textinput import TextInput  # Kullanıcının yazı yazabileceği TextInput widget'ını import ediyoruz
from kivy.uix.button import Button  # Buton widget'ını import ediyoruz
from kivy.uix.floatlayout import FloatLayout  # Elemanları serbest bir şekilde yerleştirebilmek için FloatLayout widget'ını import ediyoruz
from io import StringIO  # Terminal çıktısını yakalamak için StringIO modülünü import ediyoruz
import contextlib  # contextlib modülünü, çıktı yönlendirmesi yapmak için import ediyoruz
import subprocess

# Kod düzenleyici ekranını temsil eden sınıf
class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super(EditorScreen, self).__init__(**kwargs)  # Ekranın başlangıç ayarlarını yapıyoruz
        self.build()  # build metodunu çağırarak ekranı oluşturuyoruz

    def build(self):
        layout = FloatLayout()  # Layout olarak FloatLayout kullanıyoruz (Serbest yerleşim düzeni)

        # Kod düzenleyici alanını oluşturuyoruz
        self.code_editor = TextInput(
            hint_text="Write your Python code here...",  # Kullanıcıya yazması için bir açıklama
            size_hint=(0.9, 0.4),  # Alanın büyüklüğü
            pos_hint={"x": 0.05, "y": 0.5},  # Konumlandırma
            multiline=True,  # Birden fazla satır yazılabilmesini sağlıyoruz
            font_size=26,  # Yazı tipi büyüklüğü
            background_color=(0.1, 0.1, 0.1, 1),  # Arka plan rengi
            foreground_color=(1, 1, 1, 1),  # Yazı rengi
        )

        # Çıkış butonunu oluşturuyoruz
        exit_button = Button(
            text="X",  # Butonun metni
            size_hint=(0.05, 0.05),  # Buton boyutu
            pos_hint={"right": 1, "top": 1},  # Butonun sağ üst köşeye yerleşmesi
            background_color=(1, 0, 0, 1),  # Kırmızı renk
        )
        exit_button.bind(on_release=self.close_app)  # Butona tıklandığında close_app fonksiyonu çalışacak

        # Pip girişi için bir TextInput alanı
        self.pip_input = TextInput(
            hint_text="Enter package name to install...",  # Kullanıcıya hangi paketi yüklemek istediğini soruyoruz
            size_hint=(0.9, 0.1),  # Alanın boyutu
            pos_hint={"x": 0.05, "y": 0.15},  # Konumlandırma
            font_size=14,  # Yazı tipi büyüklüğü
            background_color=(0.1, 0.1, 0.1, 1),  # Arka plan rengi
            foreground_color=(1, 1, 1, 1),  # Yazı rengi
        )

        # "Run Code" butonunu oluşturuyoruz
        run_button = Button(
            text="Run Code",  # Buton metni
            size_hint=(0.3, 0.1),  # Buton boyutu
            pos_hint={"x": 0.05, "y": 0.05},  # Buton konumu
            on_release=self.run_code  # Butona basıldığında run_code fonksiyonu çalışacak
        )

        # "Install Library" butonunu oluşturuyoruz
        pip_button = Button(
            text="Install Library",  # Buton metni
            size_hint=(0.3, 0.1),  # Buton boyutu
            pos_hint={"x": 0.35, "y": 0.05},  # Buton konumu
            on_release=self.install_library  # Butona basıldığında install_library fonksiyonu çalışacak
        )

        # Layout'a widget'ları ekliyoruz
        layout.add_widget(self.code_editor)
        layout.add_widget(self.pip_input)
        layout.add_widget(run_button)
        layout.add_widget(pip_button)
        layout.add_widget(exit_button)

        self.add_widget(layout)  # Bu düzeni ekrana ekliyoruz

    def close_app(self, instance):
        App.get_running_app().stop()  # Uygulama kapanacak

    def run_code(self, instance):
        # Kullanıcıdan yazılmış Python kodunu alıyoruz
        user_code = self.code_editor.text

        # Terminal çıktısını yakalamak için StringIO kullanıyoruz
        output = StringIO()
        with contextlib.redirect_stdout(output):  # Çıktıyı StringIO'ya yönlendiriyoruz
            try:
                # Kullanıcı kodunu çalıştırıyoruz
                exec(user_code)
            except Exception as e:  # Hata olursa, hatayı terminal çıktısına yazıyoruz
                output.write(f"Error: {str(e)}")
        
        # Çıktıyı terminal ekranına geçiş yaparak gösteriyoruz
        terminal_screen = self.manager.get_screen('terminal')  # Terminal ekranını alıyoruz
        terminal_screen.update_output(output.getvalue())  # Terminal ekranında çıktı göster
        self.manager.current = 'terminal'  # Ekranlar arası geçiş yapıyoruz

    def install_library(self, instance):
        # Pip ile kütüphane yükleme işlemi yapacağız
        package_name = self.pip_input.text  # Kullanıcıdan paket adını alıyoruz
        if package_name:  # Eğer bir paket adı varsa
            # Terminal ekranını alıyoruz
            terminal_screen = self.manager.get_screen('terminal')
            terminal_screen.update_output(f"Installing {package_name}...")  # Terminal çıktısına yükleme işlemi yazıyoruz

            try:
                # subprocess ile pip komutunu çalıştırıyoruz
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                terminal_screen.update_output(f"Successfully installed {package_name}.")
            except subprocess.CalledProcessError as e:
                terminal_screen.update_output(f"Error installing {package_name}: {e}")
        else:
            terminal_screen = self.manager.get_screen('terminal')
            terminal_screen.update_output("Please enter a package name.")  # Eğer paket adı girilmemişse, kullanıcıyı uyarıyoruz

# Terminal ekranını temsil eden sınıf
class TerminalScreen(Screen):
    def __init__(self, **kwargs):
        super(TerminalScreen, self).__init__(**kwargs)  # Ekranın başlangıç ayarlarını yapıyoruz
        self.build()  # build metodunu çağırarak ekranı oluşturuyoruz

    def build(self):
        layout = FloatLayout()  # Layout olarak FloatLayout kullanıyoruz

        # Terminal çıktısı için bir TextInput alanı oluşturuyoruz
        self.terminal_output = TextInput(
            text="Terminal output will appear here...",  # Başlangıçta bir mesaj
            size_hint=(0.9, 0.8),  # Alanın büyüklüğü
            pos_hint={"x": 0.05, "y": 0.1},  # Konumlandırma
            readonly=True,  # Sadece okuma (yazma yapılmayacak)
            font_size=26,  # Yazı tipi büyüklüğü
            background_color=(0.2, 0.2, 0.2, 1),  # Arka plan rengi
            foreground_color=(0, 1, 0, 1),  # Yazı rengi (yeşil)
        )

        layout.add_widget(self.terminal_output)  # Layout'a terminal çıktısı ekliyoruz
        self.add_widget(layout)  # Bu düzeni ekrana ekliyoruz

    def update_output(self, text):
        # Terminal çıktısını güncellemek için fonksiyon
        self.terminal_output.text = text  # Gelen metni terminal çıktısına yazıyoruz

# Uygulama yönetimi
class PythonIDEApp(App):
    def build(self):
        sm = ScreenManager()  # Ekranları yönetmek için ScreenManager kullanıyoruz

        # Ekranları ekliyoruz
        sm.add_widget(EditorScreen(name='editor'))  # Kod düzenleyici ekranı
        sm.add_widget(TerminalScreen(name='terminal'))  # Terminal ekranı

        return sm  # Ekran yöneticisini geri döndürüyoruz

if __name__ == "__main__":
    PythonIDEApp().run()  # Uygulamayı çalıştırıyoruz
    
