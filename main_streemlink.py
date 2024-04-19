import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import streamlink
import os

class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)

    def __init__(self, url, path):
        super().__init__()
        self.url = url
        self.path = path
        self.running = True

    def run(self):
        ffmpeg_path = "/path/to/ffmpeg"
        options = {
           "ffmpeg-ffmpeg": ffmpeg_path,
    
        }
        streamlink_obj = streamlink.Streamlink(options=options)
        streams = streamlink_obj.streams(self.url)
        stream = streams['best']
        with stream.open() as stream_fd:
            with open(self.path, 'wb') as f:
                self.progress_signal.emit('다운로드 중...')
                for data in stream_fd:
                    if not self.running:  # running이 False이면 루프를 중지
                        break
                    f.write(data)
        if self.running:
            self.progress_signal.emit('다운로드 완료')
        else:
            self.progress_signal.emit('다운로드 중지')

    def stop(self):
        self.running = False

class App(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle('유튜브 다운로더')
    self.resize(400, 100)
    self.layout = QVBoxLayout()
    self.label = QLabel('URL:')
    self.url = QLineEdit()
    self.layout.addWidget(self.label)
    self.layout.addWidget(self.url)

    self.label_path  = QLabel('Path:')
    self.path = QLineEdit()
    self.browseButton = QPushButton('Browse')
    self.browseButton.clicked.connect(self.browse)
    self.pathLayout = QHBoxLayout()
    self.pathLayout.addWidget(self.path)
    self.pathLayout.addWidget(self.browseButton)

    self.downloadButton = QPushButton('Download')
    self.downloadButton.clicked.connect(self.start_download)
    self.stopButton = QPushButton('Stop Download')
    self.stopButton.clicked.connect(self.stop_download)

    self.statusLabel = QLabel('')  # 다운로드 상태를 표시하는 레이블

    self.layout.addWidget(self.label_path)
    self.layout.addLayout(self.pathLayout)
    self.layout.addWidget(self.downloadButton)
    self.layout.addWidget(self.stopButton)
    self.layout.addWidget(self.statusLabel)  # 레이블을 레이아웃에 추가
    self.setLayout(self.layout)

  def browse(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        self.path.setText(path)

  def start_download(self):
    url = self.url.text()
    path = self.path.text()
    self.download_thread = DownloadThread(url, path+'/output.mp4')
    self.download_thread.progress_signal.connect(self.update_status)
    self.download_thread.start()

  def update_status(self, status):
    self.statusLabel.setText(status)
  
  def stop_download(self):
    if hasattr(self, 'download_thread'):
      self.download_thread.stop()
      self.statusLabel.setText('다운로드 중지...')
       

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  ex.show()
  sys.exit(app.exec_())