import sys
import random
import string
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QSlider, QCheckBox, QLineEdit, 
                            QHBoxLayout, QGraphicsOpacityEffect)
from PyQt5.QtCore import (Qt, QPropertyAnimation, QEasingCurve, QTimer, 
                         QSize, QUrl)
from PyQt5.QtGui import (QFont, QColor, QPalette, QPixmap, QPainter, 
                        QLinearGradient, QIcon)
from PyQt5.QtMultimedia import QSoundEffect

class CastlePasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_sounds()
        self.show_welcome_screen()
        
    def setup_window(self):
        self.setWindowTitle("🔐 Sands of Password")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: rgba(20, 12, 8, 200);")
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_layout)
        
        # Background image
        self.background = QLabel()
        self.background.setPixmap(QPixmap("castle_bg.webp").scaled(800, 600))  # Replace with your image
        self.background.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.background)
        
        # Overlay widget for UI elements
        self.ui_overlay = QWidget()
        self.ui_overlay.setStyleSheet("background: transparent;")
        self.ui_layout = QVBoxLayout()
        self.ui_layout.setContentsMargins(50, 50, 50, 50)
        self.ui_overlay.setLayout(self.ui_layout)
        self.main_layout.addWidget(self.ui_overlay)
        
    def setup_sounds(self):
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("sword_clash.mp3"))  # Replace with your sound
        
        self.disappear_sound = QSoundEffect()
        self.disappear_sound.setSource(QUrl.fromLocalFile("disappear.mp3"))  # Replace with your sound
        
    def show_welcome_screen(self):
        # Clear existing widgets
        self.clear_layout(self.ui_layout)
        
        # Welcome title
        title = QLabel("SANDS OF PASSWORD")
        title.setFont(QFont("Times New Roman", 32, QFont.Bold))
        title.setStyleSheet("color: #e0c070; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "The ancient castle guards its secrets well.\n"
            "Generate powerful passwords to unlock its treasures.\n\n"
            "Select character types to summon guardian soldiers.\n"
            "The more soldiers you summon, the stronger your password!"
        )
        desc.setFont(QFont("Times New Roman", 14))
        desc.setStyleSheet("color: #d0b060; background: transparent;")
        desc.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(desc)
        
        # Proceed button
        proceed_btn = QPushButton("ENTER THE CASTLE")
        proceed_btn.setFont(QFont("Times New Roman", 16, QFont.Bold))
        proceed_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #805020, stop:1 #a07030);
                color: #f0e0b0;
                border: 2px solid #604010;
                border-radius: 5px;
                padding: 15px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a07030, stop:1 #805020);
            }
        """)
        proceed_btn.clicked.connect(self.show_generator)
        self.ui_layout.addWidget(proceed_btn, 0, Qt.AlignCenter)
        
    def show_generator(self):
        self.click_sound.play()
        self.clear_layout(self.ui_layout)
        
        # Soldiers row
        self.soldiers_row = QHBoxLayout()
        self.soldiers_row.setAlignment(Qt.AlignCenter)
        self.soldiers = []
        
        soldier_images = ["soldier1.webp", "soldier2.webp", "soldier3.webp", "soldier4.webp"]  # Replace with your images
        
        for img in soldier_images:
            soldier = QLabel()
            soldier.setPixmap(QPixmap(img).scaled(80, 120, Qt.KeepAspectRatio))
            soldier.setStyleSheet("background: transparent;")
            self.soldiers.append(soldier)
            self.soldiers_row.addWidget(soldier)
            
        self.ui_layout.addLayout(self.soldiers_row)
        
        # Password display
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setAlignment(Qt.AlignCenter)
        self.password_display.setFont(QFont("Courier New", 16))
        self.password_display.setStyleSheet("""
            QLineEdit {
                background: rgba(40, 20, 10, 180);
                border: 2px solid #a07030;
                border-radius: 5px;
                color: #f0e0b0;
                padding: 10px;
                selection-background-color: #a07030;
            }
        """)
        self.ui_layout.addWidget(self.password_display)
        
        # Length slider
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setRange(8, 32)
        self.length_slider.setValue(16)
        self.length_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #604010;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #a07030;
                width: 20px;
                margin: -6px 0;
                border-radius: 10px;
                border: 2px solid #402010;
            }
        """)
        self.ui_layout.addWidget(QLabel("Password Length:"))
        self.ui_layout.addWidget(self.length_slider)
        
        # Checkboxes (each represents a soldier)
        self.checks = {
            "uppercase": QCheckBox("Uppercase Guards (A-Z)"),
            "lowercase": QCheckBox("Lowercase Guards (a-z)"),
            "numbers": QCheckBox("Numerical Guards (0-9)"),
            "symbols": QCheckBox("Symbolic Guards (!@#)")
        }
        
        for i, (name, checkbox) in enumerate(self.checks.items()):
            checkbox.setChecked(True)
            checkbox.setFont(QFont("Times New Roman", 12))
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: #f0e0b0;
                    background: transparent;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border: 2px solid #a07030;
                    border-radius: 3px;
                    background: #402010;
                }
                QCheckBox::indicator:checked {
                    background: #a07030;
                }
            """)
            checkbox.stateChanged.connect(lambda state, idx=i: self.toggle_soldier(state, idx))
            self.ui_layout.addWidget(checkbox)
        
        # Generate button
        self.generate_btn = QPushButton("SUMMON PASSWORD")
        self.generate_btn.setFont(QFont("Times New Roman", 14, QFont.Bold))
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #805020, stop:1 #a07030);
                color: #f0e0b0;
                border: 2px solid #604010;
                border-radius: 5px;
                padding: 15px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a07030, stop:1 #805020);
            }
        """)
        self.generate_btn.clicked.connect(self.generate_password)
        self.ui_layout.addWidget(self.generate_btn, 0, Qt.AlignCenter)
        
    def toggle_soldier(self, state, soldier_idx):
        soldier = self.soldiers[soldier_idx]
        
        if state == Qt.Checked:
            # Soldier appears
            soldier.show()
            anim = QPropertyAnimation(soldier, b"geometry")
            anim.setDuration(500)
            anim.setStartValue(soldier.geometry().translated(0, 100))
            anim.setEndValue(soldier.geometry())
            anim.setEasingCurve(QEasingCurve.OutBack)
            anim.start()
        else:
            # Soldier disappears
            self.disappear_sound.play()
            anim = QPropertyAnimation(soldier, b"geometry")
            anim.setDuration(500)
            anim.setStartValue(soldier.geometry())
            anim.setEndValue(soldier.geometry().translated(0, 100))
            anim.setEasingCurve(QEasingCurve.InBack)
            anim.finished.connect(lambda: soldier.hide())
            anim.start()
        
    def generate_password(self):
        self.click_sound.play()
        
        # Get parameters
        length = self.length_slider.value()
        char_sets = {
            'uppercase': string.ascii_uppercase if self.checks['uppercase'].isChecked() else '',
            'lowercase': string.ascii_lowercase if self.checks['lowercase'].isChecked() else '',
            'numbers': string.digits if self.checks['numbers'].isChecked() else '',
            'symbols': string.punctuation if self.checks['symbols'].isChecked() else ''
        }
        
        # Build character pool
        chars = ''.join(char_sets.values())
        
        if not chars:
            self.password_display.setText("Summon at least one guard type!")
            return
            
        # Generate password
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_display.setText(password)
        
        # Animate the display
        self.animate_password_display()
        
    def animate_password_display(self):
        anim = QPropertyAnimation(self.password_display, b"geometry")
        anim.setDuration(200)
        anim.setStartValue(self.password_display.geometry().adjusted(-5, -5, 5, 5))
        anim.setEndValue(self.password_display.geometry())
        anim.setEasingCurve(QEasingCurve.OutElastic)
        anim.start()
        
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    window = CastlePasswordGenerator()
    window.show()
    
    sys.exit(app.exec_())