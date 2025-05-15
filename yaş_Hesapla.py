import sys
import hashlib
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sqlite3
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Veritabanı bağlantısı
baglanti = sqlite3.connect("urunler.db")
islem = baglanti.cursor()



# Kullanıcılar tablosu oluşturma
islem.execute("""
CREATE TABLE IF NOT EXISTS kullanicilar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullaniciAdi TEXT UNIQUE,
    sifre TEXT,
    email TEXT,
    yetki TEXT DEFAULT 'kullanici'
)
""")

# Örnek admin kullanıcısını ekleme (eğer yoksa)
admin_sifre = hashlib.sha256("1234".encode()).hexdigest()
islem.execute("SELECT * FROM kullanicilar WHERE kullaniciAdi = ?", ("admin",))
if not islem.fetchone():
    islem.execute(
        "INSERT INTO kullanicilar (kullaniciAdi, sifre, email, yetki) VALUES (?, ?, ?, ?)",
        ("admin", admin_sifre, "admin@example.com", "admin"),
    )

baglanti.commit()
# Kullanıcı verilerini saklamak için basit bir sözlük (kullanıcı adı: şifre)
users = {}

# Başlangıç penceresi
class StartWindow(QWidget):
    def __init__(self):    
        super().__init__()
        self.setWindowTitle("Giriş Seçenekleri")
        self.setGeometry(100, 100, 350, 220)
        
        layout = QVBoxLayout()

        title = QLabel("Hoşgeldiniz")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.btn_new_login = QPushButton("Giriş Yap")
        self.btn_new_login.clicked.connect(self.open_login)

        self.btn_existing_login = QPushButton("Zaten Giriş Yapmıştım")
        self.btn_existing_login.clicked.connect(self.open_main)

        self.btn_register = QPushButton("Kayıt Ol")
        self.btn_register.clicked.connect(self.open_register)

        self.btn_İnfo = QPushButton("Ne İşe Yarar?")
        self.btn_İnfo.clicked.connect(self.open_info)

        
        layout.addWidget(self.btn_new_login)
        layout.addWidget(self.btn_existing_login)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.btn_İnfo)

        layout.addStretch()
        self.setLayout(layout)

    def open_login(self):
        login_window.show()
        self.close()

    def open_main(self):
        main_window.show()
        self.close()

    def open_register(self):
        register_window.show()
        self.close()

    def open_info(self):
     self.info_window = InfoWindow(self)
     self.info_window.show()
     self.close()


# Kullanıcı giriş ekranı
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Girişi")
        self.setGeometry(100, 100, 350, 300)
        
        layout = QVBoxLayout()

        title = QLabel("Giriş Bilgileri")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.label_user = QLabel("Kullanıcı Adı:")
        self.input_user = QLineEdit()

        self.label_password = QLabel("Şifre:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Giriş Yap")
        self.btn_login.clicked.connect(self.login)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

def login(self):
    username = self.input_user.text()
    password = self.input_password.text()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    islem.execute(
        "SELECT * FROM kullanicilar WHERE kullaniciAdi = ? AND sifre = ?",
        (username, hashed_password)
    )
    result = islem.fetchone()

    if result:
        main_window.show()
        self.close()
    else:
        QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre!")


class InfoWindow(QWidget):
    def __init__(self, start_window):
        super().__init__()
        self.start_window = start_window

        self.setWindowTitle("Uygulama Hakkında")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        info_label = QLabel("""
Bu uygulamada istediginiz bir hayvanı arayabilir, ve yanında verilmiş olan katsayılar ıle insan yasina oranla yasini bulabilirsiniz.
Ayrıca bir hesap makinesi ile basit matematik işlemleri yapabilir, ve kullanıcı kaydı oluşturabilirsiniz. İşlemi şu şekilde yapabilirsiniz:
      1.önce giriş yapmalısınız.
      2. Giriş yaptıktan sonra istediginiz hayvanı aratın ve formulde kullanıcagımız katsayıyı öğrenin.
      3. Hesap makinesi kısmına geçin ve aradığınız hayvanın yaşını hesaplayın.
        """)
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignTop)

        # 🔙 Geri dön butonu
        back_button = QPushButton("Geri Dön")
        back_button.clicked.connect(self.back_to_start)

        layout.addWidget(info_label)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def back_to_start(self):
        self.start_window.show()
        self.close()

# Kayıt ekranı
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(100, 100, 350, 300)
        
        layout = QVBoxLayout()

        title = QLabel("Kayıt Bilgileri")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.label_user = QLabel("Kullanıcı Adı:")
        self.input_user = QLineEdit()

        self.label_password = QLabel("Şifre:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.label_confirm_password = QLabel("Şifreyi Onayla:")
        self.input_confirm_password = QLineEdit()
        self.input_confirm_password.setEchoMode(QLineEdit.Password)

        self.btn_register = QPushButton("Kayıt Ol")
        self.btn_register.clicked.connect(self.register)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_confirm_password)
        layout.addWidget(self.input_confirm_password)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

def register(self):
    username = self.input_user.text()
    password = self.input_password.text()
    confirm_password = self.input_confirm_password.text()

    if password != confirm_password:
        QMessageBox.warning(self, "Hata", "Şifreler eşleşmiyor!")
        return

    if username and password:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            islem.execute(
                "INSERT INTO kullanicilar (kullaniciAdi, sifre, email) VALUES (?, ?, ?)",
                (username, hashed_password, username + "@mail.com")  # Basit e-posta örneği
            )
            baglanti.commit()
            QMessageBox.information(self, "Başarılı", "Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
            start_window.show()
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten mevcut!")
    else:
        QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")


# Ana menü ekranı
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ana Menü")
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()

        title = QLabel("Ana Menü")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.btn_calc = QPushButton("Hesap Makinesi")
        self.btn_calc.clicked.connect(self.open_calculator)

        self.btn_search = QPushButton("En Sevdiğin Hayvanı Bul")
        self.btn_search.clicked.connect(self.open_search)

        layout.addWidget(self.btn_calc)
        layout.addWidget(self.btn_search)
        self.setLayout(layout)

    def open_calculator(self):
        self.calc_window = CalculatorWindow()
        self.calc_window.show()

    def open_search(self):
        self.search_window = SearchWindow()
        self.search_window.show()

# Hesap makinesi ekranı
class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hesap Makinesi")
        self.setGeometry(100, 100, 300, 350)
        
        layout = QVBoxLayout()

        self.result_label = QLabel("0")
        self.result_label.setFont(QFont("Segoe UI", 16))
        self.result_label.setAlignment(Qt.AlignRight)

        self.input_field = QLineEdit()

        self.buttons_layout = QGridLayout()
        self.buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
        ]

        for text, row, col in self.buttons:
            button = QPushButton(text)
            button.clicked.connect(self.on_button_click)
            self.buttons_layout.addWidget(button, row, col)

        layout.addWidget(self.result_label)
        layout.addWidget(self.input_field)
        layout.addLayout(self.buttons_layout)
        self.setLayout(layout)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        if text == "=":
            try:
                result = eval(self.input_field.text())
                self.result_label.setText(str(result))
            except Exception:
                self.result_label.setText("Hata")
        else:
            self.input_field.setText(self.input_field.text() + text)

# Kelime arama ekranı
class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kelime Arama")
        self.setGeometry(100, 100, 300, 250)

        self.words = ["aslan: 5.36", "kartal: 2.5", "fare: 37.5", "kedi: 5", "kopek: 6.25", "kangal: 6.8", "zurafa: 3", "balina: 0.94", "geyık: 6.25", "kurt: 5.77", "sinek: 750", "dogan: 5", "maymun: 2.5", "tavsan: 8.33", "timsah: 1.07", "kaplumbaga: 0.94", "kurbaga: 7.5", "karga: 3.75", "kuzgun: 3", "serce: 25", "kirlangic: 15"
]

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Kelime Arama"))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Kelimeyi giriniz...")
        self.search_button = QPushButton("Ara")
        self.search_button.clicked.connect(self.search_word)

        self.result_list = QListWidget()

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_list)

        self.setLayout(layout)

    def search_word(self):
        search_term = self.search_input.text().strip().lower()
        self.result_list.clear()

        results = [word for word in self.words if search_term in word.lower()]
        if results:
            self.result_list.addItems(results)
        else:
            self.result_list.addItem("Sonuç bulunamadı!")

# Uygulama başlatılır
app = QApplication(sys.argv)
app.setStyleSheet("""
    QWidget {
        background-color: #f0f0f5;
        font-family: 'Segoe UI';
        font-size: 14px;
    }

    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }

    QPushButton:hover {
        background-color: #45a049;
    }

    QLineEdit, QDateEdit {
        padding: 6px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: white;
    }

    QLabel {
        font-weight: bold;
    }

    QListWidget {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    QRadioButton {
        padding: 3px;
    }
""")

start_window = StartWindow()
login_window = LoginWindow()
register_window = RegisterWindow()
main_window = MainWindow()
start_window.show()
sys.exit(app.exec())
