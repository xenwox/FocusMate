from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont


class PomodoroManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.work_time = 25 * 60  # 25 dakika
        self.short_break = 5 * 60  # 5 dakika
        self.long_break = 15 * 60  # 15 dakika
        self.timer_seconds = self.work_time
        self.is_running = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        layout = QVBoxLayout()

        # Zaman label
        self.time_label = QLabel(self.format_time(self.timer_seconds))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont("San Francisco", 36, QFont.Bold))
        layout.addWidget(self.time_label)

        # Butonlar
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("▶️ Başlat")
        self.start_btn.clicked.connect(self.start_timer)
        btn_layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton("⏸️ Duraklat")
        self.pause_btn.clicked.connect(self.pause_timer)
        btn_layout.addWidget(self.pause_btn)

        self.reset_btn = QPushButton("🔄 Sıfırla")
        self.reset_btn.clicked.connect(self.reset_timer)
        btn_layout.addWidget(self.reset_btn)

        layout.addLayout(btn_layout)

        # Molalar
        break_layout = QHBoxLayout()
        self.short_break_btn = QPushButton("☕ Kısa Mola")
        self.short_break_btn.clicked.connect(self.start_short_break)
        break_layout.addWidget(self.short_break_btn)

        self.long_break_btn = QPushButton("🛌 Uzun Mola")
        self.long_break_btn.clicked.connect(self.start_long_break)
        break_layout.addWidget(self.long_break_btn)

        layout.addLayout(break_layout)

        self.setLayout(layout)

    # Zaman formatı mm:ss
    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    # Timer güncelle
    def update_timer(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.time_label.setText(self.format_time(self.timer_seconds))
        else:
            self.timer.stop()
            self.is_running = False
            QMessageBox.information(self, "Pomodoro", "⏰ Süre doldu!")

    # Başlat
    def start_timer(self):
        if not self.is_running:
            self.timer.start(1000)
            self.is_running = True

    # Duraklat
    def pause_timer(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False

    # Sıfırla
    def reset_timer(self):
        self.timer.stop()
        self.timer_seconds = self.work_time
        self.time_label.setText(self.format_time(self.timer_seconds))
        self.is_running = False

    # Kısa mola
    def start_short_break(self):
        self.timer.stop()
        self.timer_seconds = self.short_break
        self.time_label.setText(self.format_time(self.timer_seconds))
        self.timer.start(1000)
        self.is_running = True

    # Uzun mola
    def start_long_break(self):
        self.timer.stop()
        self.timer_seconds = self.long_break
        self.time_label.setText(self.format_time(self.timer_seconds))
        self.timer.start(1000)
        self.is_running = True
