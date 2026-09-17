import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp


# =========================================================
# DATABASE SQLITE
# =========================================================

DB_NAME = "medika_plus.db"

DOKTER = [
    ("Dr. Andi Pratama", "Dokter Umum"),
    ("Dr. Siti Rahma", "Dokter Anak"),
    ("Dr. Budi Santoso", "Dokter Gigi"),
    ("Dr. Rina Lestari", "Dokter Umum"),
    ("Dr. Dimas Wijaya", "Dokter Penyakit Dalam"),
]


def init_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS dokter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL UNIQUE,
            spesialis TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS janji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pasien TEXT NOT NULL,
            umur INTEGER NOT NULL,
            dokter TEXT NOT NULL,
            tanggal TEXT NOT NULL,
            jam TEXT NOT NULL,
            keluhan TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Terjadwal'
        )
    """)

    for nama, spesialis in DOKTER:
        cur.execute(
            """
            INSERT OR IGNORE INTO dokter
            (nama, spesialis)
            VALUES (?, ?)
            """,
            (nama, spesialis)
        )

    conn.commit()
    conn.close()


# =========================================================
# MENAMBAHKAN JANJI KE DATABASE
# =========================================================

def tambah_janji(
    nama,
    umur,
    dokter,
    tanggal,
    jam,
    keluhan
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM janji
        WHERE dokter = ?
        AND tanggal = ?
        AND jam = ?
    """, (dokter, tanggal, jam))

    jumlah = cur.fetchone()[0]

    if jumlah > 0:
        conn.close()
        return False, "JADWAL SUDAH PENUH"

    cur.execute("""
        INSERT INTO janji
        (
            nama_pasien,
            umur,
            dokter,
            tanggal,
            jam,
            keluhan,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nama,
        umur,
        dokter,
        tanggal,
        jam,
        keluhan,
        "Terjadwal"
    ))

    conn.commit()
    conn.close()

    return True, "Data berhasil disimpan."


# =========================================================
# MENGAMBIL DATA JANJI
# =========================================================

def ambil_janji():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            nama_pasien,
            umur,
            dokter,
            tanggal,
            jam,
            keluhan,
            status
        FROM janji
        ORDER BY tanggal, jam
    """)

    data = cur.fetchall()
    conn.close()
    return data


# =========================================================
# MENGHAPUS SEMUA DATA
# =========================================================

def hapus_semua():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM janji")
    conn.commit()
    conn.close()


# =========================================================
# CEK KETERSEDIAAN JADWAL
# =========================================================

def cek_ketersediaan(
    dokter,
    tanggal,
    jam
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM janji
        WHERE dokter = ?
        AND tanggal = ?
        AND jam = ?
    """, (dokter, tanggal, jam))

    jumlah = cur.fetchone()[0]
    conn.close()

    if jumlah > 0:
        return False

    return True


# =========================================================
# WIDGET CARD
# =========================================================

class Card(BoxLayout):
    def __init__(
        self,
        bg_color=(1, 1, 1, 1),
        **kwargs
    ):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self.rectangle = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[15]
            )
        self.bind(
            pos=self.update_rectangle,
            size=self.update_rectangle
        )

    def update_rectangle(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size


# =========================================================
# TOMBOL CUSTOM
# =========================================================

def create_button(
    text,
    color,
    height=50
):
    button = Button(
        text=text,
        font_size=15,
        bold=True,
        size_hint_y=None,
        height=dp(height),
        background_normal="",
        background_color=color,
        color=(1, 1, 1, 1)
    )
    return button


# =========================================================
# INPUT CUSTOM
# =========================================================

def create_input(
    hint,
    height=48
):
    return TextInput(
        hint_text=hint,
        multiline=False,
        size_hint_y=None,
        height=dp(height),
        padding=[15, 12],
        font_size=14
    )


# =========================================================
# WIDGET LOGO KLINIK KUSTOM
# =========================================================

class ClinicLogo(BoxLayout):
    """Widget dekoratif untuk menggambar logo klinik medis (Palang Merah)"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(80), dp(80))
        
        with self.canvas:
            Color(1, 1, 1, 1)
            self.bg_circle = RoundedRectangle(pos=self.pos, size=self.size, radius=[40])
            
            Color(0.85, 0.15, 0.15, 1)
            self.v_bar = Rectangle(pos=(self.x + dp(32), self.y + dp(18)), size=(dp(16), dp(44)))
            self.h_bar = Rectangle(pos=(self.x + dp(18), self.y + dp(32)), size=(dp(44), dp(16)))
            
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_circle.pos = self.pos
        self.bg_circle.size = self.size
        self.v_bar.pos = (self.x + self.width/2 - dp(8), self.y + self.height/2 - dp(22))
        self.h_bar.pos = (self.x + self.width/2 - dp(22), self.y + self.height/2 - dp(8))


# =========================================================
# HALAMAN BERANDA
# =========================================================

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main = BoxLayout(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(15)
        )

        with main.canvas.before:
            Color(0.93, 0.96, 0.99, 1)
            self.bg = RoundedRectangle(
                pos=main.pos,
                size=main.size
            )

        main.bind(
            pos=lambda obj, value: setattr(self.bg, "pos", value),
            size=lambda obj, value: setattr(self.bg, "size", value)
        )

        header_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(140),
            spacing=dp(10)
        )
        header_layout.bind(width=lambda obj, w: setattr(logo_container, 'x', (w - logo_container.width) / 2))

        logo_container = BoxLayout(size_hint=(None, None), size=(dp(80), dp(80)), pos_hint={'center_x': 0.5})
        logo_container.add_widget(ClinicLogo())
        header_layout.add_widget(logo_container)

        title = Label(
            text="MEDIKA PLUS",
            font_size=28,
            bold=True,
            halign="center",
            color=(0.05, 0.25, 0.55, 1),
            size_hint_y=None,
            height=dp(35)
        )
        title.bind(size=title.setter('text_size'))
        header_layout.add_widget(title)

        main.add_widget(header_layout)

        subtitle = Label(
            text="SMART HEALTHCARE APPOINTMENT",
            font_size=13,
            bold=True,
            halign="center",
            color=(0.12, 0.50, 0.40, 1),
            size_hint_y=None,
            height=dp(25)
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        main.add_widget(subtitle)

        desc_card = Card(
            padding=dp(12),
            size_hint_y=None,
            height=dp(60),
            bg_color=(1, 1, 1, 0.8)
        )
        desc_label = Label(
            text="Atur konsultasi dengan dokter secara mudah,\ncepat, dan terstruktur.",
            font_size=13,
            halign="center",
            valign="middle",
            color=(0.3, 0.3, 0.3, 1)
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        desc_card.add_widget(desc_label)
        main.add_widget(desc_card)

        # Menu Tombol Navigasi (Tanpa Simbol/Kotak di Kiri)
        btn_dokter = create_button("DAFTAR DOKTER", (0.10, 0.48, 0.82, 1), 48)
        btn_dokter.bind(on_press=lambda x: setattr(self.manager, "current", "dokter"))
        main.add_widget(btn_dokter)

        btn_janji = create_button("BUAT JANJI KONSULTASI", (0.08, 0.62, 0.45, 1), 48)
        btn_janji.bind(on_press=lambda x: setattr(self.manager, "current", "janji"))
        main.add_widget(btn_janji)

        btn_data = create_button("DATA JANJI SAYA", (0.45, 0.25, 0.70, 1), 48)
        btn_data.bind(on_press=lambda x: setattr(self.manager, "current", "data"))
        main.add_widget(btn_data)

        btn_info = create_button("INFORMASI KESEHATAN", (0.85, 0.50, 0.15, 1), 48)
        btn_info.bind(on_press=lambda x: setattr(self.manager, "current", "tips"))
        main.add_widget(btn_info)

        self.add_widget(main)


# =========================================================
# DAFTAR DOKTER
# =========================================================

class DokterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12)
        )

        title = Label(
            text="DAFTAR DOKTER",
            font_size=24,
            bold=True,
            color=(0.04, 0.30, 0.65, 1),
            size_hint_y=None,
            height=dp(50)
        )
        main.add_widget(title)

        scroll = ScrollView()
        doctors = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )
        doctors.bind(minimum_height=doctors.setter("height"))

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT nama, spesialis FROM dokter ORDER BY id")
        daftar = cur.fetchall()
        conn.close()

        for nama, spesialis in daftar:
            card = Card(
                orientation="vertical",
                padding=dp(14),
                spacing=dp(4),
                size_hint_y=None,
                height=dp(95),
                bg_color=(0.90, 0.95, 1, 1)
            )

            card.add_widget(
                Label(
                    text=nama,
                    font_size=17,
                    bold=True,
                    color=(0.04, 0.28, 0.55, 1),
                    halign="left"
                )
            )

            card.add_widget(
                Label(
                    text=spesialis,
                    font_size=14,
                    color=(0.3, 0.3, 0.3, 1),
                    halign="left"
                )
            )

            doctors.add_widget(card)

        scroll.add_widget(doctors)
        main.add_widget(scroll)

        back = create_button("KEMBALI", (0.40, 0.42, 0.48, 1), 48)
        back.bind(on_press=lambda x: setattr(self.manager, "current", "home"))
        main.add_widget(back)

        self.add_widget(main)


# =========================================================
# HALAMAN BUAT JANJI
# =========================================================

class JanjiScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(8)
        )

        title = Label(
            text="BUAT JANJI KONSULTASI",
            font_size=22,
            bold=True,
            color=(0.04, 0.30, 0.65, 1),
            size_hint_y=None,
            height=dp(45)
        )
        main.add_widget(title)

        self.nama = create_input("Masukkan nama pasien")
        self.umur = create_input("Masukkan umur")
        self.umur.input_filter = "int"

        self.dokter = Spinner(
            text="Pilih dokter",
            values=[dokter[0] for dokter in DOKTER],
            size_hint_y=None,
            height=dp(48),
            font_size=14
        )

        self.tanggal = create_input("Tanggal (YYYY-MM-DD)")
        self.jam = create_input("Jam (contoh: 09:00)")

        self.keluhan = TextInput(
            hint_text="Tuliskan keluhan atau keperluan konsultasi",
            multiline=True,
            size_hint_y=None,
            height=dp(80),
            padding=[12, 12],
            font_size=14
        )

        main.add_widget(self.nama)
        main.add_widget(self.umur)
        main.add_widget(self.dokter)
        main.add_widget(self.tanggal)
        main.add_widget(self.jam)
        main.add_widget(self.keluhan)

        cek = create_button("CEK KETERSEDIAAN JADWAL", (0.10, 0.48, 0.75, 1), 44)
        cek.bind(on_press=self.cek_jadwal)
        main.add_widget(cek)

        simpan = create_button("SIMPAN JANJI", (0.08, 0.62, 0.42, 1), 46)
        simpan.bind(on_press=self.simpan_janji)
        main.add_widget(simpan)

        back = create_button("KEMBALI", (0.40, 0.42, 0.48, 1), 44)
        back.bind(on_press=lambda x: setattr(self.manager, "current", "home"))
        main.add_widget(back)

        self.status = Label(
            text="",
            font_size=13,
            bold=True,
            color=(0.05, 0.50, 0.25, 1),
            size_hint_y=None,
            height=dp(30)
        )
        main.add_widget(self.status)

        self.add_widget(main)

    def cek_jadwal(self, instance):
        dokter = self.dokter.text
        tanggal = self.tanggal.text.strip()
        jam = self.jam.text.strip()

        if dokter == "Pilih dokter" or not tanggal or not jam:
            self.status.text = "Isi dokter, tanggal, dan jam terlebih dahulu."
            self.status.color = (0.8, 0.1, 0.1, 1)
            return

        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            datetime.strptime(jam, "%H:%M")
        except ValueError:
            self.status.text = "Format salah. Contoh: 2026-09-20 | 09:00"
            self.status.color = (0.8, 0.1, 0.1, 1)
            return

        if cek_ketersediaan(dokter, tanggal, jam):
            self.status.text = "JADWAL TERSEDIA - Silakan simpan."
            self.status.color = (0.05, 0.50, 0.25, 1)
        else:
            self.status.text = "JADWAL SUDAH PENUH - Pilih jam lain."
            self.status.color = (0.85, 0.15, 0.08, 1)

    def simpan_janji(self, instance):
        if not self.nama.text.strip() or not self.umur.text.strip() or self.dokter.text == "Pilih dokter":
            self.status.text = "Mohon lengkapi formulir dengan benar."
            self.status.color = (0.8, 0.1, 0.1, 1)
            return

        tanggal = self.tanggal.text.strip()
        jam = self.jam.text.strip()

        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            datetime.strptime(jam, "%H:%M")
        except ValueError:
            self.status.text = "Format tanggal/jam salah."
            self.status.color = (0.8, 0.1, 0.1, 1)
            return

        berhasil, pesan = tambah_janji(
            self.nama.text.strip(),
            int(self.umur.text),
            self.dokter.text,
            tanggal,
            jam,
            self.keluhan.text.strip()
        )

        if not berhasil:
            self.status.text = "JADWAL SUDAH PENUH"
            self.status.color = (0.85, 0.12, 0.08, 1)
            return

        self.status.text = "JANJI BERHASIL DISIMPAN"
        self.status.color = (0.05, 0.50, 0.25, 1)

        self.nama.text = ""
        self.umur.text = ""
        self.dokter.text = "Pilih dokter"
        self.tanggal.text = ""
        self.jam.text = ""
        self.keluhan.text = ""


# =========================================================
# DATA JANJI
# =========================================================

class DataScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )
        self.add_widget(self.main)

    def on_enter(self):
        self.main.clear_widgets()

        title = Label(
            text="DATA JANJI KONSULTASI",
            font_size=24,
            bold=True,
            color=(0.04, 0.30, 0.65, 1),
            size_hint_y=None,
            height=dp(50)
        )
        self.main.add_widget(title)

        data = ambil_janji()
        scroll = ScrollView()
        daftar = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )
        daftar.bind(minimum_height=daftar.setter("height"))

        if not data:
            daftar.add_widget(
                Label(
                    text="Belum ada data janji konsultasi.",
                    font_size=15,
                    size_hint_y=None,
                    height=dp(50)
                )
            )
        else:
            for nomor, item in enumerate(data, start=1):
                id_data, nama, umur, dokter, tanggal, jam, keluhan, status = item

                card = Card(
                    orientation="vertical",
                    padding=dp(12),
                    spacing=dp(3),
                    size_hint_y=None,
                    height=dp(170),
                    bg_color=(0.94, 0.97, 1, 1)
                )

                info = (
                    f"JANJI #{nomor} | {status}\n"
                    f"Pasien : {nama} ({umur} thn)\n"
                    f"Dokter : {dokter}\n"
                    f"Waktu  : {tanggal} {jam}\n"
                    f"Keluhan: {keluhan}"
                )

                card.add_widget(
                    Label(
                        text=info,
                        font_size=13,
                        color=(0.15, 0.15, 0.15, 1),
                        halign="left",
                        valign="middle"
                    )
                )
                daftar.add_widget(card)

        scroll.add_widget(daftar)
        self.main.add_widget(scroll)

        hapus = create_button("HAPUS SEMUA DATA", (0.82, 0.18, 0.18, 1), 46)
        hapus.bind(on_press=self.hapus_data)
        self.main.add_widget(hapus)

        back = create_button("KEMBALI", (0.40, 0.42, 0.48, 1), 46)
        back.bind(on_press=lambda x: setattr(self.manager, "current", "home"))
        self.main.add_widget(back)

    def hapus_data(self, instance):
        hapus_semua()
        self.on_enter()


# =========================================================
# INFORMASI KESEHATAN
# =========================================================

class TipsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12)
        )

        title = Label(
            text="INFORMASI KESEHATAN",
            font_size=24,
            bold=True,
            color=(0.04, 0.30, 0.65, 1),
            size_hint_y=None,
            height=dp(50)
        )
        main.add_widget(title)

        informasi = [
            "Konsumsi makanan yang beragam dan bergizi.",
            "Cukupi kebutuhan cairan tubuh setiap hari.",
            "Lakukan aktivitas fisik secara teratur.",
            "Istirahat dan tidur dengan cukup.",
            "Jaga kebersihan diri dan lingkungan.",
            "Jika mengalami keluhan kesehatan, konsultasikan segera."
        ]

        scroll = ScrollView()
        isi = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )
        isi.bind(minimum_height=isi.setter("height"))

        for teks in informasi:
            card = Card(
                padding=dp(12),
                size_hint_y=None,
                height=dp(70),
                bg_color=(1, 0.97, 0.88, 1)
            )
            card.add_widget(
                Label(
                    text=teks,
                    font_size=14,
                    color=(0.25, 0.25, 0.25, 1),
                    halign="left"
                )
            )
            isi.add_widget(card)

        scroll.add_widget(isi)
        main.add_widget(scroll)

        back = create_button("KEMBALI", (0.40, 0.42, 0.48, 1), 48)
        back.bind(on_press=lambda x: setattr(self.manager, "current", "home"))
        main.add_widget(back)

        self.add_widget(main)


# =========================================================
# APLIKASI UTAMA
# =========================================================

class MedikaPlusApp(App):
    def build(self):
        init_database()
        self.title = "Medika Plus - Smart Healthcare"

        manager = ScreenManager()
        manager.add_widget(HomeScreen(name="home"))
        manager.add_widget(DokterScreen(name="dokter"))
        manager.add_widget(JanjiScreen(name="janji"))
        manager.add_widget(DataScreen(name="data"))
        manager.add_widget(TipsScreen(name="tips"))

        return manager


# =========================================================
# MENJALANKAN PROGRAM
# =========================================================

if __name__ == "__main__":
    MedikaPlusApp().run()