import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QTextEdit, QLineEdit, QHBoxLayout, QMessageBox

NOTES_FILE = "data/notes.json"

class NotesManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Not dosyasını oluştur
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "w") as f:
                json.dump([], f)

        # Arayüz
        layout = QVBoxLayout()

        # Not listesi
        self.notes_list = QListWidget()
        layout.addWidget(self.notes_list)

        # Not başlığı ve içerik
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Not başlığı")
        layout.addWidget(self.title_input)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Not içeriği")
        layout.addWidget(self.content_input)

        # Butonlar
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Not Ekle")
        self.add_btn.clicked.connect(self.add_note)
        btn_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("🗑️ Not Sil")
        self.delete_btn.clicked.connect(self.delete_note)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.load_notes()

    # Notları yükle
    def load_notes(self):
        self.notes_list.clear()
        with open(NOTES_FILE, "r") as f:
            self.notes_data = json.load(f)
        for note in self.notes_data:
            self.notes_list.addItem(note["title"])

    # Yeni not ekle
    def add_note(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        if not title:
            QMessageBox.warning(self, "Hata", "Not başlığı boş olamaz!")
            return
        new_note = {"title": title, "content": content}
        self.notes_data.append(new_note)
        with open(NOTES_FILE, "w") as f:
            json.dump(self.notes_data, f, indent=4)
        self.load_notes()
        self.title_input.clear()
        self.content_input.clear()

    # Not sil
    def delete_note(self):
        selected_items = self.notes_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Hata", "Silinecek not seçin!")
            return
        for item in selected_items:
            for note in self.notes_data:
                if note["title"] == item.text():
                    self.notes_data.remove(note)
                    break
        with open(NOTES_FILE, "w") as f:
            json.dump(self.notes_data, f, indent=4)
        self.load_notes()
