from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QRadioButton
from PyQt5.QtCore import QThread, pyqtSignal
from downloader import download_audio, download_video
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QRadioButton, QGroupBox, QHBoxLayout
from pytube import YouTube

class Downloader(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, url, path, is_audio):
        QThread.__init__(self)
        self.url = url
        self.path = path
        self.is_audio = is_audio

    def run(self):
        try:
            yt = YouTube(self.url)
            yt.register_on_progress_callback(self.on_progress)
            if self.is_audio:
                result = download_audio(yt, self.path)
            else:
                result = download_video(yt, self.path)
            self.signal.emit(result)

        except Exception as e:
            print("에러: " + e)
            self.signal.emit("Error: " + str(e))

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining

        percentage_of_completion = int(bytes_downloaded / total_size * 100)
        self.signal.emit(f"다운로드 : {percentage_of_completion}%")

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'YouTube Downloader'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.resize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        url_group = QGroupBox("YouTube URL")
        url_layout = QHBoxLayout()
        url_group.setLayout(url_layout)

        self.url_entry = QLineEdit()
        url_layout.addWidget(self.url_entry)

        path_group = QGroupBox("Save Path")
        path_layout = QHBoxLayout()
        path_group.setLayout(path_layout)

        self.path_entry = QLineEdit()
        path_layout.addWidget(self.path_entry)

        options_group = QGroupBox("Options")
        options_layout = QHBoxLayout()
        options_group.setLayout(options_layout)

        self.audio_button = QRadioButton("Audio")
        self.audio_button.setChecked(True)
        self.video_button = QRadioButton("Video")

        options_layout.addWidget(self.audio_button)
        options_layout.addWidget(self.video_button)

        self.result_label = QLabel()

        download_button = QPushButton('Download', self)
        download_button.clicked.connect(self.start_download_thread)

        layout.addWidget(url_group)
        layout.addWidget(path_group)
        layout.addWidget(options_group)
        layout.addWidget(download_button)
        layout.addWidget(self.result_label)

    def start_download_thread(self):
        self.downloader = Downloader(self.url_entry.text(), self.path_entry.text(), self.audio_button.isChecked())
        self.downloader.signal.connect(self.update_label)
        self.downloader.finished.connect(self.downloader.deleteLater)
        self.downloader.start()

    def update_label(self, text):
        self.result_label.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
