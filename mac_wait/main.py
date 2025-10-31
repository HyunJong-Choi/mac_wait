import sys
import os
import signal
import psutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from pynput import keyboard

# macOS용 시그널 값 정의 (혹시 누락된 경우 대비)
SIGSTOP = getattr(signal, "SIGSTOP", 19)
SIGCONT = getattr(signal, "SIGCONT", 18)

class AppController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("macOS 앱 제어기")
        self.resize(400, 400)

        self.layout = QVBoxLayout()
        self.label = QLabel("실행 중인 앱 목록 (선택 후 아래 버튼 클릭)")
        self.layout.addWidget(self.label)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.refresh_button = QPushButton("🔄 새로고침")
        self.layout.addWidget(self.refresh_button)

        self.selected_pid = None

        self.refresh_button.clicked.connect(self.load_apps)
        self.list_widget.itemClicked.connect(self.select_app)

        self.setLayout(self.layout)
        self.load_apps()

        # 키보드 리스너 실행
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def load_apps(self):
        """현재 실행 중인 프로세스 목록 표시"""
        self.list_widget.clear()
        for p in psutil.process_iter(['pid', 'name']):
            try:
                if p.info['name'] and not p.info['name'].startswith("com.apple.") and p.info['name'].startswith("Maple"):
                    self.list_widget.addItem(f"{p.info['name']} (PID: {p.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def select_app(self, item):
        """리스트에서 앱 선택"""
        text = item.text()
        pid = int(text.split("PID: ")[1].replace(")", ""))
        self.selected_pid = pid
        QMessageBox.information(self, "선택됨", f"선택한 앱 PID: {pid}\nA: 일시정지 / B: 재개")

    def on_key_press(self, key):
        """A / B 키 입력 처리"""
        if not self.selected_pid:
            return
        try:
            if key.char.lower() == 'a':
                os.kill(self.selected_pid, SIGSTOP)
                print(f"[✅] PID {self.selected_pid} 일시정지")
            elif key.char.lower() == 'b':
                os.kill(self.selected_pid, SIGCONT)
                print(f"[🚀] PID {self.selected_pid} 재개")
        except AttributeError:
            pass
        except ProcessLookupError:
            print("❌ 해당 PID의 프로세스가 존재하지 않습니다.")

    def closeEvent(self, event):
        """앱 종료 시 리스너도 정리"""
        self.listener.stop()
        event.accept()


def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = AppController()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
