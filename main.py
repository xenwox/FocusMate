import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QStackedWidget, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QPoint

# Modüller import (hazır olduğunda aktif olur)
from backup import BackupManager
from notes import NotesManager
from pomodoro import PomodoroManager
from project_manager import ProjectManager
from schedule import ScheduleManager
from password_manager import PasswordManager


class HoverButton(QWidget):
    """Sağ menü için hover efektli buton"""
    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)

        # İkon
        self.icon_label = QLabel()
        self.icon_label.setPixmap(
            QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Yazı
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("font-size: 11pt; color: #333;")
        self.text_label.setVisible(False)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.text_label, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)

        # Boyut ve stil
        self.setFixedWidth(100)
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
            QWidget:hover {
                background-color: #e6f0ff;
                border-radius: 10px;
            }
        """)

    def enterEvent(self, event):
        self.text_label.setVisible(True)
        anim = QPropertyAnimation(self.icon_label, b"pos")
        anim.setDuration(200)
        anim.setStartValue(self.icon_label.pos())
        anim.setEndValue(self.icon_label.pos() - QPoint(10, 0))
        anim.start()
        self.anim = anim
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.text_label.setVisible(False)
        anim = QPropertyAnimation(self.icon_label, b"pos")
        anim.setDuration(200)
        anim.setStartValue(self.icon_label.pos())
        anim.setEndValue(self.icon_label.pos() + QPoint(10, 0))
        anim.start()
        self.anim = anim
        super().leaveEvent(event)


class FocusMateMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FocusMate v1.3")
        self.setFixedSize(1200, 700)
        self.setWindowIcon(QIcon("icon.png"))

        # Ana widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Sağ Menü
        self.menu_layout = QVBoxLayout()
        self.menu_layout.setAlignment(Qt.AlignCenter)
        self.menu_buttons = []

        # İçerik alanı (modüller için)
        self.stack = QStackedWidget()
        self.module_instances = {}

        modules = [
            ("Projeler", ProjectManager, "icons/project.png"),
            ("Pomodoro", PomodoroManager, "icons/pomodoro.png"),
            ("Notlar", NotesManager, "icons/notes.png"),
            ("Çizelge", ScheduleManager, "icons/schedule.png"),
            ("Yedekleme", BackupManager, "icons/backup.png"),
            ("Şifre Kasası", PasswordManager, "icons/password.png")
        ]

        # Menü butonları ekle
        for name, cls, icon in modules:
            btn = HoverButton(icon, name)
            btn.mousePressEvent = lambda event, n=name, c=cls: self.load_module(n, c)
            self.menu_layout.addWidget(btn)
            self.menu_buttons.append(btn)

            # Placeholder
            placeholder = QWidget()
            ph_layout = QVBoxLayout()
            lbl = QLabel(f"{name} modülü yükleniyor...")
            lbl.setFont(QFont("Arial", 12))
            lbl.setAlignment(Qt.AlignCenter)
            ph_layout.addWidget(lbl)
            placeholder.setLayout(ph_layout)
            self.stack.addWidget(placeholder)

        # Layout yerleşimi
        self.menu_layout.addStretch()
        self.main_layout.addWidget(self.stack, 4)
        self.main_layout.addLayout(self.menu_layout, 1)

        self.statusBar().showMessage("FocusMate v1.3 Hazır")

    # Lazy load modüller
    def load_module(self, name, cls):
        if name not in self.module_instances:
            widget = cls(self)
            self.module_instances[name] = widget
            self.stack.addWidget(widget)
        self.stack.setCurrentWidget(self.module_instances[name])
        self.statusBar().showMessage(f"{name} modülü açık")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FocusMateMainWindow()
    window.show()
    sys.exit(app.exec_())
