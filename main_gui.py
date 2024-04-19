from PyQt5.QtWidgets import * 
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import yt_dlp
import sys
import os
import signal

class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)
    

    def __init__(self, url, path, audio_only):
        super().__init__()
        self.url = url
        self.path = path
        self.audio_only = audio_only
        self.process = None
        

    def run(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        ffmpeg_path = os.path.join(base_path, 'ffmpeg.exe')
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': self.path + '/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
            'ffmpeg_location': ffmpeg_path,
            'noplaylist' : True,
        }

        if self.audio_only:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if self.is_live_video(self.url):
                self.progress_signal.emit('라이브 방송은 다운로드 할 수 없습니다.')
                return
            ydl.download([self.url])

        self.progress_signal.emit('다운로드 완료')

    def is_live_video(self, url):
        """
        주어진 URL의 영상이 라이브 스트리밍인지 확인합니다.
        라이브 스트리밍이면 True, 아니면 False를 반환합니다.
        """
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            # 라이브 스트리밍 여부를 확인합니다.
            return info_dict.get('is_live') or info_dict.get('was_live')
    
    def progress_hook(self, d):
      p = d['_percent_str']
      percent_index = p.find('%')
      space_index = p.rfind(' ', 0, percent_index)
      if space_index != -1:
        p = p[space_index+1:percent_index]
        self.progress_signal.emit(f'다운로드 중... {p}%')
    

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the window icon
        if getattr(sys, 'frozen', False):
            # Running as a bundled executable
            base_path = sys._MEIPASS
        else:
            # Running as a normal Python script
            base_path = os.path.dirname(__file__)
        self.setWindowIcon(QIcon(os.path.join(base_path, 'Icon.ico')))

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
        self.audioOnlyCheckbox = QCheckBox('음원만 받기')
        self.downloadButton = QPushButton('Download')
        self.downloadButton.clicked.connect(self.download)

        self.statusLabel = QLabel('')  # 다운로드 상태를 표시하는 레이블

        self.layout.addWidget(self.label_path)
        self.layout.addLayout(self.pathLayout)
        
        self.layout.addWidget(self.audioOnlyCheckbox)
        self.layout.addWidget(self.downloadButton)
        self.layout.addWidget(self.statusLabel)  # 레이블을 레이아웃에 추가
        self.setLayout(self.layout)

    def browse(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        self.path.setText(path)

    def download(self):
        url = self.url.text()
        path = self.path.text()
        audio_only = self.audioOnlyCheckbox.isChecked()
        self.downloadThread = DownloadThread(url, path, audio_only)
        self.downloadThread.progress_signal.connect(self.update_status)
        self.downloadThread.start()
        self.statusLabel.setText('다운로드 시작...')

            

    def update_status(self, status):
        self.statusLabel.setText(status)

app = QApplication([])
ex = App()
ex.show()
sys.exit(app.exec_())