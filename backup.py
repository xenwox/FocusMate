import os
import shutil
import json
import hashlib
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QVBoxLayout, QPushButton


CONFIG_FILE = "data/backup_paths.json"
BACKUP_DIR = "data/backups/"


class BackupManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Yedek klasörlerini oluştur
        os.makedirs(BACKUP_DIR, exist_ok=True)
        if not os.path.exists(CONFIG_FILE):
            os.makedirs("data", exist_ok=True)
            with open(CONFIG_FILE, "w") as f:
                json.dump({"paths": []}, f)

        # Arayüz
        layout = QVBoxLayout()

        self.add_folder_btn = QPushButton("📁 Klasör Ekle")
        self.add_folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.add_folder_btn)

        self.run_backup_btn = QPushButton("▶️ Yedekleme Çalıştır")
        self.run_backup_btn.clicked.connect(self.backup)
        layout.addWidget(self.run_backup_btn)

        self.setLayout(layout)

        # Otomatik yedekleme
        self.auto_backup()

    # JSON’dan klasörleri oku
    def load_paths(self):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)["paths"]

    # JSON’a kaydet
    def save_paths(self, paths):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"paths": paths}, f, indent=4)

    # Klasör seçme
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Klasör Seç")
        if folder:
            paths = self.load_paths()
            if folder not in paths:
                paths.append(folder)
                self.save_paths(paths)
                QMessageBox.information(self, "Yedekleme", f"{folder}\n📂 yedeklenecek klasörlere eklendi.")
            else:
                QMessageBox.information(self, "Yedekleme", "Bu klasör zaten listede var ✅")

    # Otomatik yedekleme
    def auto_backup(self):
        paths = self.load_paths()
        if paths:  # Eğer yedeklenecek klasör varsa
            self.backup(auto=True)

    # Yedekleme işlemi
    def backup(self, auto=False):
        paths = self.load_paths()
        if not paths:
            if not auto:
                QMessageBox.warning(self, "Yedekleme", "Henüz yedeklenecek klasör seçilmedi!")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        target_dir = os.path.join(BACKUP_DIR, timestamp)
        os.makedirs(target_dir, exist_ok=True)

        any_file_copied = False

        for path in paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        src = os.path.join(root, file)
                        rel_path = os.path.relpath(src, path)
                        dest = os.path.join(target_dir, os.path.basename(path), rel_path)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)

                        if not os.path.exists(dest) or not self.same_file(src, dest):
                            shutil.copy2(src, dest)
                            any_file_copied = True

        if not auto:
            QMessageBox.information(self, "Yedekleme", "✅ Yedekleme tamamlandı")
        else:
            if any_file_copied:
                print("Otomatik yedekleme: Yeni dosyalar yedeklendi ✅")
            else:
                print("Otomatik yedekleme: Yeni dosya yok, işlem yapılmadı.")

    # Dosya karşılaştırma
    def same_file(self, f1, f2):
        return self.hash_file(f1) == self.hash_file(f2)

    def hash_file(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()


