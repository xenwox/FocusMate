import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QHBoxLayout, QLabel, QStackedWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

# Modülleri import et
from project_manager import ProjectManager
from pomodoro import PomodoroManager
from notes import NotesManager
from schedule import ScheduleManager
from backup import BackupManager
from password_manager import PasswordManager

class FocusMateMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FocusMate v1.0")
        self.setFixedSize(1200, 800)
        self.setWindowIcon(QIcon("icon.png"))

        self.modules = {}  # Lazy loading için modül saklama

        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Sol Menü
        menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        menu_widget.setLayout(menu_layout)
        menu_widget.setFixedWidth(200)
        menu_layout.setAlignment(Qt.AlignCenter)
        menu_layout.setSpacing(15)

        # Menü Butonları
        buttons_info = [
            ("Projeler", "📁", "projeler"),
            ("Pomodoro", "⏳", "pomodoro"),
            ("Notlar", "📝", "notlar"),
            ("Çizelge", "📆", "çizelge"),
            ("Backup", "💾", "backup"),
            ("Şifre Kasası", "🔐", "sifre"),
        ]

        for text, icon, key in buttons_info:
            btn = QPushButton(f"{icon}  {text}")
            btn.setFont(QFont("San Francisco", 12))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #f0f0f0; 
                    border-radius: 10px; 
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                """
            )
            btn.clicked.connect(lambda checked, k=key: self.show_module(k))
            menu_layout.addWidget(btn)

        main_layout.addWidget(menu_widget)

        # Ana Alan
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack, 1)

        # Üst Başlık
        title = QLabel("FocusMate v1.0 - Günlük Planlama ve Proje Takibi")
        title.setFont(QFont("San Francisco", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2C3E50;")
        self.statusBar().showMessage("Hazır")
        self.stack.addWidget(title)

    def show_module(self, name):
        if name not in self.modules:
            if name == "projeler":
                self.modules[name] = ProjectManager()
            elif name == "pomodoro":
                self.modules[name] = PomodoroManager()
            elif name == "notlar":
                self.modules[name] = NotesManager()
            elif name == "çizelge":
                self.modules[name] = ScheduleManager()
            elif name == "backup":
                self.modules[name] = BackupManager()
            elif name == "sifre":
                self.modules[name] = PasswordManager()
            self.stack.addWidget(self.modules[name])
        self.stack.setCurrentWidget(self.modules[name])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FocusMateMainWindow()
    window.show()
    sys.exit(app.exec_())
