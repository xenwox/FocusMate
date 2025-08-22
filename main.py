from backup import BackupManager
from pomodoro import PomodoroManager
from notes import NotesManager
from schedule import ScheduleManager
from password_manager import PasswordManager
from project_manager import ProjectManager




import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QListWidget, QHBoxLayout, QMessageBox, QStackedWidget
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

class FocusMateMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FocusMate - Dijital Ajanda")
        self.setFixedSize(1200, 800)
        self.setWindowIcon(QIcon("assets/icon.png"))

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Başlık
        self.title_label = QLabel("📔 FocusMate - Dijital Ajanda")
        self.title_label.setFont(QFont("San Francisco", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #2C3E50; margin: 20px;")
        self.main_layout.addWidget(self.title_label)

        # İçerik düzeni (sol buton paneli + sağ modül alanı)
        self.content_layout = QHBoxLayout()

        # Sol panel (Butonlar)
        self.button_layout = QVBoxLayout()
        self.add_button("📁 Projeler", 0)
        self.add_button("⏳ Pomodoro", 1)
        self.add_button("📝 Notlar", 2)
        self.add_button("📆 Çizelge", 3)
        self.add_button("📂 Yedekleme", 4)
        self.add_button("🔐 Şifre Kasası", 5)
        self.button_layout.addStretch()
        self.content_layout.addLayout(self.button_layout, 1)

        # Sağ panel (QStackedWidget)
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #F8F9FA; border-radius: 10px;")
        self.content_layout.addWidget(self.stack, 4)

        # Her modül için sayfalar ekle

        self.stack.addWidget(ProjectManager(self))  # 📁 Projeler gerçek modül
        self.stack.addWidget(PomodoroManager(self))  # ✅ Pomodoro gerçek ekran
        self.stack.addWidget(NotesManager(self)) # ✅ Notlar gerçek ekran
        self.stack.addWidget(ScheduleManager(self)) # ✅ Çizelge gerçek ekran
        self.stack.addWidget(BackupManager(self))   # ✅ Gerçek backup ekranı
        self.stack.addWidget(PasswordManager(self))  # ✅ Şifre Kasası gerçek ekran



        self.main_layout.addLayout(self.content_layout)

        # Status bar
        self.statusBar().showMessage("Hazır")

    # Buton oluşturma
    def add_button(self, text, index):
        btn = QPushButton(text)
        btn.setFont(QFont("San Francisco", 14))
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: #007AFF; 
                color: white; 
                border-radius: 12px; 
                padding: 12px;
                margin: 5px;
            }
            QPushButton:hover { background-color: #005BB5; }
            """
        )
        btn.clicked.connect(lambda: self.switch_page(index))
        self.button_layout.addWidget(btn)

    # Placeholder sayfa
    def module_placeholder(self, title):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel(title)
        label.setFont(QFont("San Francisco", 20, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    # Sayfa geçiş animasyonu
    def switch_page(self, index):
        current_index = self.stack.currentIndex()
        if current_index == index:
            return

        # Animasyon efekti (slide)
        current_widget = self.stack.currentWidget()
        next_widget = self.stack.widget(index)

        geo = self.stack.geometry()
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()

        # Yeni widget pozisyon dışı başlat
        next_widget.setGeometry(QRect(w, 0, w, h))
        self.stack.setCurrentIndex(index)

        anim = QPropertyAnimation(next_widget, b"geometry")
        anim.setDuration(500)
        anim.setStartValue(QRect(w, 0, w, h))
        anim.setEndValue(QRect(0, 0, w, h))
        anim.start()

        self.statusBar().showMessage(f"{index+1}. modül açıldı")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FocusMateMainWindow()
    window.show()
    sys.exit(app.exec_())
