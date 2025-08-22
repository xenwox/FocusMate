import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QListWidget,
    QLabel, QFileDialog, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt

PROJECT_FILE = "data/projects.json"

class ProjectManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        os.makedirs("data", exist_ok=True)
        if not os.path.exists(PROJECT_FILE):
            with open(PROJECT_FILE, "w") as f:
                json.dump({}, f)

        self.data = {}
        self.load_projects()

        layout = QVBoxLayout()

        # Proje listesi
        self.project_list = QListWidget()
        self.project_list.itemClicked.connect(self.show_project_details)
        layout.addWidget(self.project_list)

        # Başlık ve açıklama
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Yeni Proje Başlığı")
        layout.addWidget(self.title_input)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Proje Açıklaması")
        layout.addWidget(self.desc_input)

        # Tamamlanma durumu
        self.completed_checkbox = QCheckBox("Proje Tamamlandı")
        layout.addWidget(self.completed_checkbox)

        # Dosya ekleme
        file_layout = QHBoxLayout()
        self.add_file_btn = QPushButton("📁 Dosya Ekle")
        self.add_file_btn.clicked.connect(self.add_file)
        file_layout.addWidget(self.add_file_btn)

        self.file_list = QListWidget()
        file_layout.addWidget(self.file_list, 3)
        layout.addLayout(file_layout)

        # Kontrol butonları
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Proje Ekle / Güncelle")
        self.add_btn.clicked.connect(self.add_or_update_project)
        btn_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("🗑️ Proje Sil")
        self.delete_btn.clicked.connect(self.delete_project)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

        # Detay alanı
        self.details_label = QLabel("Proje detayları burada gösterilecek")
        self.details_label.setAlignment(Qt.AlignTop)
        self.details_label.setWordWrap(True)
        layout.addWidget(self.details_label)

        self.setLayout(layout)
        self.refresh_list()

    # --- Veri işlemleri ---
    def load_projects(self):
        with open(PROJECT_FILE, "r") as f:
            self.data = json.load(f)

    def save_projects(self):
        with open(PROJECT_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def refresh_list(self):
        self.project_list.clear()
        for title, info in self.data.items():
            status = "✅" if info.get("completed") else "❌"
            self.project_list.addItem(f"{status} {title}")

    # --- Proje ekleme/güncelleme ---
    def add_or_update_project(self):
        title = self.title_input.text().strip()
        desc = self.desc_input.toPlainText().strip()
        completed = self.completed_checkbox.isChecked()
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]

        if not title:
            QMessageBox.warning(self, "Hata", "Proje başlığı boş olamaz!")
            return

        self.data[title] = {
            "description": desc,
            "completed": completed,
            "files": files,
            "last_updated": datetime.now().isoformat()
        }
        self.save_projects()
        self.refresh_list()
        self.clear_inputs()

    def delete_project(self):
        selected_items = self.project_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Hata", "Silinecek projeyi seçin!")
            return
        for item in selected_items:
            title = item.text()[2:]  # ✅/❌ simgesini çıkar
            self.data.pop(title, None)
        self.save_projects()
        self.refresh_list()
        self.details_label.setText("Proje detayları burada gösterilecek")

    def show_project_details(self, item):
        title = item.text()[2:]  # simgeyi çıkar
        info = self.data.get(title, {})
        files = "\n".join(info.get("files", []))
        status = "Tamamlandı ✅" if info.get("completed") else "Tamamlanmadı ❌"
        last_updated = info.get("last_updated", "Bilinmiyor")
        desc = info.get("description", "")
        self.details_label.setText(
            f"<b>{title}</b>\n\nDurum: {status}\nGüncelleme: {last_updated}\n\nAçıklama:\n{desc}\n\nDosyalar:\n{files}"
        )

        # Formu doldur
        self.title_input.setText(title)
        self.desc_input.setText(desc)
        self.completed_checkbox.setChecked(info.get("completed", False))
        self.file_list.clear()
        for f in info.get("files", []):
            self.file_list.addItem(f)

    def clear_inputs(self):
        self.title_input.clear()
        self.desc_input.clear()
        self.completed_checkbox.setChecked(False)
        self.file_list.clear()

    # --- Dosya ekleme ---
    def add_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç")
        if file_path:
            if file_path not in [self.file_list.item(i).text() for i in range(self.file_list.count())]:
                self.file_list.addItem(file_path)
