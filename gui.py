from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QRadioButton
from PyQt5.QtCore import QThread, pyqtSignal
from downloader import download_audio, download_video
import sys

class Downloader(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, url, path, is_audio):
        QThread.__init__(self)
        self.url = url
        self.path = path
        self.is_audio = is_audio

    def run(self):
        try:
            if self.is_audio:
                result = download_audio(self.url, self.path)
            else:
                result = download_video(self.url, self.path)
            self.signal.emit(result)

        except Exception as e:
            print("에러: " + e)
            self.signal.emit("Error: " + str(e))

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'YouTube Downloader'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.url_entry = QLineEdit()
        self.path_entry = QLineEdit()

        self.audio_button = QRadioButton("Audio")
        self.audio_button.setChecked(True)
        self.video_button = QRadioButton("Video")

        self.result_label = QLabel()

        download_button = QPushButton('Download', self)
        download_button.clicked.connect(self.start_download_thread)

        layout.addWidget(QLabel("YouTube URL:"))
        layout.addWidget(self.url_entry)

        layout.addWidget(QLabel("Save Path:"))
        layout.addWidget(self.path_entry)

        layout.addWidget(self.audio_button)
        layout.addWidget(self.video_button)

        layout.addWidget(download_button)
        layout.addWidget(self.result_label)

    def start_download_thread(self):
        downloader = Downloader(self.url_entry.text(), self.path_entry.text(), self.audio_button.isChecked())
        downloader.signal.connect(self.update_label)
        downloader.start()

    def update_label(self, text):
        self.result_label.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())