from pytube import YouTube
from moviepy.editor import *

def download_audio(youtube_link, save_path):
    try:
        yt = YouTube(youtube_link)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(save_path)

        clip = AudioFileClip(out_file)
        clip.write_audiofile(out_file.replace(".mp4", ".wav"))

        print("다운로드 완료: " + out_file)
        return "Audio download 완료: " + out_file

    except Exception as e:
        print("에러: " + str(e))
        return "Error: " + str(e)

def download_video(youtube_link, save_path):
    try:
        yt = YouTube(youtube_link)
        video = yt.streams.first()
        out_file = video.download(save_path)

        print("다운로드 완료: " + out_file)
        return "Video download 완료: " + out_file

    except Exception as e:
        print("에러: " + e)
        return "Error: " + str(e)
    

download_audio("https://www.youtube.com/watch?v=INak4ORss18", "C:/Users/akshw/바탕 화면/test")