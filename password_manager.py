import os
import json
import base64
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QMessageBox
)
from cryptography.fernet import Fernet
from hashlib import sha256

PASSWORD_FILE = "data/passwords.json"

class PasswordManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        os.makedirs("data", exist_ok=True)
        if not os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, "w") as f:
                json.dump({}, f)

        layout = QVBoxLayout()

        # Ana parola girişi
        self.master_input = QLineEdit()
        self.master_input.setEchoMode(QLineEdit.Password)
        self.master_input.setPlaceholderText("Ana parolayı gir")
        layout.addWidget(self.master_input)

        self.unlock_btn = QPushButton("🔓 Kilidi Aç")
        self.unlock_btn.clicked.connect(self.unlock)
        layout.addWidget(self.unlock_btn)

        # Şifre listesi ve ekleme
        self.password_list = QListWidget()
        layout.addWidget(self.password_list)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Başlık")
        layout.addWidget(self.title_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        layout.addWidget(self.password_input)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Ekle")
        self.add_btn.clicked.connect(self.add_password)
        btn_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("🗑️ Sil")
        self.delete_btn.clicked.connect(self.delete_password)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.fernet = None
        self.data = {}

    # Ana parola ile key oluştur (SHA256 -> base64)
    def generate_key(self, master_password):
        key_hash = sha256(master_password.encode()).digest()
        return base64.urlsafe_b64encode(key_hash)

    # Ana parola ile giriş
    def unlock(self):
        master = self.master_input.text()
        if not master:
            QMessageBox.warning(self, "Hata", "Ana parola boş olamaz!")
            return

        self.fernet = Fernet(self.generate_key(master))

        try:
            with open(PASSWORD_FILE, "r") as f:
                encrypted_data = json.load(f)

            self.data = {}
            for k, v in encrypted_data.items():
                decrypted_username = self.fernet.decrypt(v["username"].encode()).decode()
                decrypted_password = self.fernet.decrypt(v["password"].encode()).decode()
                self.data[k] = {"username": decrypted_username, "password": decrypted_password}

            self.load_passwords()
            QMessageBox.information(self, "Başarılı", "✅ Şifreler yüklendi")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Şifreler yüklenemedi: {e}")

    def load_passwords(self):
        self.password_list.clear()
        for k in self.data.keys():
            self.password_list.addItem(k)

    def add_password(self):
        if not self.fernet:
            QMessageBox.warning(self, "Hata", "Önce ana parolayla kilidi açın!")
            return

        title = self.title_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not title or not password:
            QMessageBox.warning(self, "Hata", "Başlık ve şifre boş olamaz!")
            return

        # Şifrele
        enc_username = self.fernet.encrypt(username.encode()).decode()
        enc_password = self.fernet.encrypt(password.encode()).decode()

        # Dosyaya kaydet
        with open(PASSWORD_FILE, "r") as f:
            encrypted_data = json.load(f)

        encrypted_data[title] = {"username": enc_username, "password": enc_password}

        with open(PASSWORD_FILE, "w") as f:
            json.dump(encrypted_data, f, indent=4)

        # Listeyi güncelle
        self.title_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.unlock()  # Şifreleri tekrar çöz ve yükle

    def delete_password(self):
        selected_items = self.password_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Hata", "Silinecek şifreyi seçin!")
            return

        with open(PASSWORD_FILE, "r") as f:
            encrypted_data = json.load(f)

        for item in selected_items:
            encrypted_data.pop(item.text(), None)

        with open(PASSWORD_FILE, "w") as f:
            json.dump(encrypted_data, f, indent=4)

        self.unlock()
