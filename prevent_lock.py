import sys
import time
from datetime import datetime
import pyautogui
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QWidget, QLabel, QSpinBox, QStyleFactory)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont

class PreventLockWorker(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, interval):
        super().__init__()
        self.interval = interval
        self.is_running = True
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.MINIMUM_SLEEP = 0
        pyautogui.PAUSE = 0

    def run(self):
        while self.is_running:
            try:
                current_time = datetime.now().strftime("%H:%M:%S")
                pyautogui.moveRel(1, 0, duration=0.01)
                pyautogui.moveRel(-1, 0, duration=0.01)
                self.update_signal.emit(f"上次操作时间: {current_time}")
                
                for _ in range(int(self.interval / 5)):
                    if not self.is_running:
                        break
                    time.sleep(5)
                    
            except Exception as e:
                self.update_signal.emit(f"发生错误: {str(e)}")
                time.sleep(5)

    def stop(self):
        self.is_running = False

class PreventLockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.initUI()

    def initUI(self):
        # 设置窗口基本属性
        self.setWindowTitle('防锁屏工具')
        self.setFixedSize(300, 400)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            QPushButton {
                background-color: #0071e3;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0077ED;
            }
            QPushButton:pressed {
                background-color: #005ECB;
            }
            QPushButton#stopButton {
                background-color: #ff3b30;
            }
            QPushButton#stopButton:hover {
                background-color: #ff453a;
            }
            QLabel {
                color: #1d1d1f;
                font-size: 13px;
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid #d2d2d7;
                border-radius: 5px;
                background: white;
                color: #1d1d1f;
                font-size: 13px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background: #f5f5f7;
                padding: 2px;
            }
        """)

        # 创建主窗口部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 30, 20, 30)

        # 标题标签
        title_label = QLabel('防锁屏工具')
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # 间隔设置
        interval_label = QLabel('移动间隔 (秒):')
        layout.addWidget(interval_label)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(30, 3600)
        self.interval_spin.setValue(290)
        layout.addWidget(self.interval_spin)

        # 状态标签
        self.status_label = QLabel('准备就绪')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # 开始按钮
        self.start_button = QPushButton('开始运行')
        self.start_button.clicked.connect(self.start_prevention)
        layout.addWidget(self.start_button)

        # 停止按钮
        self.stop_button = QPushButton('停止运行')
        self.stop_button.setObjectName('stopButton')
        self.stop_button.clicked.connect(self.stop_prevention)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        # 添加弹性空间
        layout.addStretch()

        # 版权信息
        copyright_label = QLabel('© 2024 防锁屏工具')
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)

    def start_prevention(self):
        interval = self.interval_spin.value()
        self.worker = PreventLockWorker(interval)
        self.worker.update_signal.connect(self.update_status)
        self.worker.start()
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.interval_spin.setEnabled(False)
        self.status_label.setText('正在运行中...')

    def stop_prevention(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait()
            self.worker = None
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.interval_spin.setEnabled(True)
        self.status_label.setText('已停止')

    def update_status(self, message):
        self.status_label.setText(message)

    def closeEvent(self, event):
        self.stop_prevention()
        event.accept()

if __name__ == '__main__':
    # 修改高 DPI 支持的设置方式
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    
    app = QApplication(sys.argv)
    window = PreventLockApp()
    window.show()
    sys.exit(app.exec()) 