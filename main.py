import yt_dlp
import signal
import sys

# 유튜브 라이브 스트림 URL
url = "https://youtu.be/66YDE3D_UxM?si=nvcp2-aLqjVSPwAC"

# 다운로드 옵션 설정
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
}

# 다운로드 중단 처리를 위한 핸들러
def signal_handler(sig, frame):
    print('다운로드 중단, 저장된 파일을 확인하세요.')
    sys.exit(0)

# SIGINT 시그널(CTRL+C)에 대한 핸들러 설정
signal.signal(signal.SIGINT, signal_handler)

# yt-dlp를 사용하여 다운로드
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print('다운로드 완료')