import psutil
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QMessageBox, QScrollArea, QListWidget, QListWidgetItem, QAbstractItemView, QGroupBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QCursor


class PythonHacker1(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Python Hacker 1')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #36393F;")

        self.process_label = QLabel('Process List', self)
        self.process_label.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold; margin-top: 10px; margin-left: 10px;")

        self.process_list = QListWidget(self)
        self.process_list.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px; margin-right: 10px; background-color: #2F3136; border-radius: 5px;")
        self.process_list.setSelectionMode(QAbstractItemView.NoSelection)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setStyleSheet("background-color: #2F3136; border-radius: 5px;")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.process_list)

        self.search_label = QLabel('Search:', self)
        self.search_label.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.search_input = QLineEdit(self)
        self.search_input.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px; background-color: #2F3136; border-radius: 5px; padding: 5px;")
        self.search_input.setPlaceholderText("Enter search query")
        self.search_input.textChanged.connect(self.filter_processes)

        self.kill_label = QLabel('Kill Process', self)
        self.kill_label.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold; margin-top: 10px; margin-left: 10px;")

        self.pid_label = QLabel('PID:', self)
        self.pid_label.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.pid_input = QLineEdit(self)
        self.pid_input.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px; background-color: #2F3136; border-radius: 5px; padding: 5px;")
        self.pid_input.setPlaceholderText("Enter PID")

        self.kill_button = QPushButton('Kill', self)
        self.kill_button.setStyleSheet("color: #FFFFFF; font-size: 14px; background-color: #7289DA; border-radius: 5px; padding: 5px;")
        self.kill_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.kill_button.clicked.connect(self.kill_process)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.setStyleSheet("color: #FFFFFF; font-size: 14px; background-color: #7289DA; border-radius: 5px; padding: 5px;")
        self.exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.exit_button.clicked.connect(self.close)

        self.cpu_label = QLabel('CPU Usage:', self)
        self.cpu_label.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.cpu_usage = QLabel(self)
        self.cpu_usage.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.ram_label = QLabel('RAM Usage:', self)
        self.ram_label.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.ram_usage = QLabel(self)
        self.ram_usage.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.network_label = QLabel('NETWORK Usage:', self)
        self.network_label.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.network_usage = QLabel(self)
        self.network_usage.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.disk_label = QLabel('DISK Usage:', self)
        self.disk_label.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.disk_usage = QLabel(self)
        self.disk_usage.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")

        self.usage_group = QGroupBox('', self)
        self.usage_group.setStyleSheet("color: #FFFFFF; font-size: 14px; margin-left: 10px;")
        usage_layout = QVBoxLayout()
        usage_layout.addWidget(self.cpu_label)
        usage_layout.addWidget(self.cpu_usage)
        usage_layout.addWidget(self.ram_label)
        usage_layout.addWidget(self.ram_usage)
        usage_layout.addWidget(self.network_label)
        usage_layout.addWidget(self.network_usage)
        usage_layout.addWidget(self.disk_label)
        usage_layout.addWidget(self.disk_usage)
        self.usage_group.setLayout(usage_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.process_label)
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.kill_label)
        layout.addWidget(self.pid_label)
        layout.addWidget(self.pid_input)
        layout.addWidget(self.kill_button)
        layout.addWidget(self.exit_button)
        layout.addWidget(self.usage_group)

        self.setLayout(layout)

        # Update process list every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_processes)
        self.timer.start(1000)

        self.processes = []
        self.update_processes()

    def update_processes(self):
        self.processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                process_info = f"{proc.info['pid']} - {proc.info['name']} - {proc.info['username']}"
                self.processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        self.filter_processes(self.search_input.text())

        # Get CPU and RAM usage
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent

        self.cpu_usage.setText(f'{cpu_percent}%')
        self.ram_usage.setText(f'{ram_percent}%')

        # Get Network usage
        network_usage = psutil.net_io_counters()
        self.network_usage.setText(f'{network_usage.bytes_sent / 1024 / 1024:.2f} MB / {network_usage.bytes_recv / 1024 / 1024:.2f} MB')

        # Get Disk usage
        disk_usage = psutil.disk_usage('/')
        self.disk_usage.setText(f'{disk_usage.used / 1024 / 1024:.2f} MB / {disk_usage.total / 1024 / 1024:.2f} MB')

    def filter_processes(self, query):
        self.process_list.clear()
        for process_info in self.processes:
            if query.lower() in process_info.lower():
                item = QListWidgetItem(process_info)
                self.process_list.addItem(item)

    def kill_process(self):
        pid = self.pid_input.text()
        try:
            process = psutil.Process(int(pid))
            process.kill()
            QMessageBox.information(self, 'Success', f'Process {pid} killed successfully.')
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            QMessageBox.warning(self, 'Error', f'Failed to kill process {pid}.')
        self.pid_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    process_manager = PythonHacker1()
    process_manager.show()
    sys.exit(app.exec_())
