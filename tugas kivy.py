from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


# =========================
# HALAMAN HOME
# =========================
class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=15
        )

        title = Label(
            text="APLIKASI DATA SISWA",
            font_size=28
        )

        subtitle = Label(
            text="Project Kivy\nMico Hanafi - TKJ",
            font_size=18
        )

        btn_mulai = Button(
            text="MULAI",
            size_hint_y=None,
            height=55
        )

        btn_tentang = Button(
            text="TENTANG",
            size_hint_y=None,
            height=55
        )

        btn_mulai.bind(
            on_press=self.buka_menu
        )

        btn_tentang.bind(
            on_press=self.buka_tentang
        )

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(btn_mulai)
        layout.add_widget(btn_tentang)

        self.add_widget(layout)

    def buka_menu(self, instance):
        self.manager.current = "menu"

    def buka_tentang(self, instance):
        self.manager.current = "tentang"


# =========================
# HALAMAN MENU
# =========================
class MenuScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=15
        )

        title = Label(
            text="MENU UTAMA",
            font_size=28
        )

        btn_data = Button(
            text="DATA SISWA",
            size_hint_y=None,
            height=55
        )

        btn_profil = Button(
            text="PROFIL",
            size_hint_y=None,
            height=55
        )

        btn_info = Button(
            text="INFORMASI",
            size_hint_y=None,
            height=55
        )

        btn_kembali = Button(
            text="KEMBALI",
            size_hint_y=None,
            height=55
        )

        btn_data.bind(
            on_press=self.buka_data
        )

        btn_profil.bind(
            on_press=self.buka_profil
        )

        btn_info.bind(
            on_press=self.buka_info
        )

        btn_kembali.bind(
            on_press=self.buka_home
        )

        layout.add_widget(title)
        layout.add_widget(btn_data)
        layout.add_widget(btn_profil)
        layout.add_widget(btn_info)
        layout.add_widget(btn_kembali)

        self.add_widget(layout)

    def buka_data(self, instance):
        self.manager.current = "data"

    def buka_profil(self, instance):
        self.manager.current = "profil"

    def buka_info(self, instance):
        self.manager.current = "info"

    def buka_home(self, instance):
        self.manager.current = "home"


# =========================
# HALAMAN DATA SISWA
# =========================
class DataScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        title = Label(
            text="FORM DATA SISWA",
            font_size=26,
            size_hint_y=None,
            height=50
        )

        self.nama = TextInput(
            hint_text="Nama",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.kelas = TextInput(
            hint_text="Kelas",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.jurusan = TextInput(
            hint_text="Jurusan",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.alamat = TextInput(
            hint_text="Alamat",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        btn_simpan = Button(
            text="SIMPAN",
            size_hint_y=None,
            height=55
        )

        btn_hapus = Button(
            text="HAPUS",
            size_hint_y=None,
            height=55
        )

        self.hasil = Label(
            text="",
            font_size=16
        )

        btn_kembali = Button(
            text="KEMBALI",
            size_hint_y=None,
            height=55
        )

        btn_simpan.bind(
            on_press=self.simpan
        )

        btn_hapus.bind(
            on_press=self.hapus
        )

        btn_kembali.bind(
            on_press=self.kembali
        )

        layout.add_widget(title)
        layout.add_widget(self.nama)
        layout.add_widget(self.kelas)
        layout.add_widget(self.jurusan)
        layout.add_widget(self.alamat)
        layout.add_widget(btn_simpan)
        layout.add_widget(btn_hapus)
        layout.add_widget(self.hasil)
        layout.add_widget(btn_kembali)

        self.add_widget(layout)

    def simpan(self, instance):

        nama = self.nama.text
        kelas = self.kelas.text
        jurusan = self.jurusan.text
        alamat = self.alamat.text

        if nama == "":
            self.hasil.text = "Nama belum diisi"
            return

        if kelas == "":
            self.hasil.text = "Kelas belum diisi"
            return

        if jurusan == "":
            self.hasil.text = "Jurusan belum diisi"
            return

        if alamat == "":
            self.hasil.text = "Alamat belum diisi"
            return

        self.hasil.text = (
            "DATA TERSIMPAN\n"
            "Nama: " + nama + "\n"
            "Kelas: " + kelas + "\n"
            "Jurusan: " + jurusan + "\n"
            "Alamat: " + alamat
        )

    def hapus(self, instance):

        self.nama.text = ""
        self.kelas.text = ""
        self.jurusan.text = ""
        self.alamat.text = ""

        self.hasil.text = "Data sudah dihapus"

    def kembali(self, instance):
        self.manager.current = "menu"


# =========================
# HALAMAN PROFIL
# =========================
class ProfilScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        title = Label(
            text="PROFIL",
            font_size=28
        )

        informasi = Label(
            text="Nama: Mico Hanafi\n"
                 "Jurusan: TKJ\n"
                 "Sekolah: SMKN 1 Kota Kediri",
            font_size=18
        )

        btn_kembali = Button(
            text="KEMBALI",
            size_hint_y=None,
            height=55
        )

        btn_kembali.bind(
            on_press=self.kembali
        )

        layout.add_widget(title)
        layout.add_widget(informasi)
        layout.add_widget(btn_kembali)

        self.add_widget(layout)

    def kembali(self, instance):
        self.manager.current = "menu"


# =========================
# HALAMAN INFORMASI
# =========================
class InfoScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        title = Label(
            text="INFORMASI",
            font_size=28
        )

        informasi = Label(
            text="Aplikasi dibuat menggunakan Python "
                 "dan Kivy.\n\n"
                 "Materi yang digunakan:\n"
                 "Navigation\n"
                 "Event Handling",
            font_size=18
        )

        btn_kembali = Button(
            text="KEMBALI",
            size_hint_y=None,
            height=55
        )

        btn_kembali.bind(
            on_press=self.kembali
        )

        layout.add_widget(title)
        layout.add_widget(informasi)
        layout.add_widget(btn_kembali)

        self.add_widget(layout)

    def kembali(self, instance):
        self.manager.current = "menu"


# =========================
# HALAMAN TENTANG
# =========================
class TentangScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        title = Label(
            text="TENTANG APLIKASI",
            font_size=28
        )

        informasi = Label(
            text="Aplikasi Data Siswa\n\n"
                 "Dibuat oleh Mico Hanafi\n"
                 "SMKN 1 Kota Kediri\n"
                 "Jurusan TKJ",
            font_size=18
        )

        btn_kembali = Button(
            text="KEMBALI",
            size_hint_y=None,
            height=55
        )

        btn_kembali.bind(
            on_press=self.kembali
        )

        layout.add_widget(title)
        layout.add_widget(informasi)
        layout.add_widget(btn_kembali)

        self.add_widget(layout)

    def kembali(self, instance):
        self.manager.current = "home"


# =========================
# APLIKASI UTAMA
# =========================
class MyApp(App):

    def build(self):

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(name="home")
        )

        manager.add_widget(
            MenuScreen(name="menu")
        )

        manager.add_widget(
            DataScreen(name="data")
        )

        manager.add_widget(
            ProfilScreen(name="profil")
        )

        manager.add_widget(
            InfoScreen(name="info")
        )

        manager.add_widget(
            TentangScreen(name="tentang")
        )

        return manager


# =========================
# MENJALANKAN PROGRAM
# =========================
if __name__ == "__main__":
    MyApp().run()