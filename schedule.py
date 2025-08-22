import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QHBoxLayout, QMessageBox, QComboBox, QLabel
from PyQt5.QtCore import Qt

SCHEDULE_FILE = "data/schedule.json"

class ScheduleManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        os.makedirs("data", exist_ok=True)
        if not os.path.exists(SCHEDULE_FILE):
            with open(SCHEDULE_FILE, "w") as f:
                json.dump({}, f)

        layout = QVBoxLayout()

        # Gün seçici
        self.day_selector = QComboBox()
        self.day_selector.addItems([
            "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"
        ])
        self.day_selector.currentIndexChanged.connect(self.load_tasks)
        layout.addWidget(QLabel("Gün Seç:"))
        layout.addWidget(self.day_selector)

        # Görev listesi
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Görev ekleme
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Görev ekle...")
        layout.addWidget(self.task_input)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Ekle")
        self.add_btn.clicked.connect(self.add_task)
        btn_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("🗑️ Sil")
        self.delete_btn.clicked.connect(self.delete_task)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.load_tasks()

    # Görevleri yükle
    def load_tasks(self):
        self.task_list.clear()
        with open(SCHEDULE_FILE, "r") as f:
            self.schedule_data = json.load(f)
        day = self.day_selector.currentText()
        tasks = self.schedule_data.get(day, [])
        for task in tasks:
            self.task_list.addItem(task)

    # Görev ekle
    def add_task(self):
        task = self.task_input.text().strip()
        if not task:
            QMessageBox.warning(self, "Hata", "Görev boş olamaz!")
            return
        day = self.day_selector.currentText()
        if day not in self.schedule_data:
            self.schedule_data[day] = []
        self.schedule_data[day].append(task)
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(self.schedule_data, f, indent=4)
        self.task_input.clear()
        self.load_tasks()

    # Görev sil
    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Hata", "Silinecek görev seçin!")
            return
        day = self.day_selector.currentText()
        for item in selected_items:
            if day in self.schedule_data and item.text() in self.schedule_data[day]:
                self.schedule_data[day].remove(item.text())
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(self.schedule_data, f, indent=4)
        self.load_tasks()
