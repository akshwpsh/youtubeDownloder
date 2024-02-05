from pytube import YouTube
from moviepy.editor import *

def download_audio(youtube_link, save_path):
    try:
        yt = YouTube(youtube_link)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(save_path)

        clip = AudioFileClip(out_file)
        clip.write_audiofile(out_file.replace(".mp4", ".wav"))

        return "Audio download 완료: " + out_file

    except Exception as e:
        return "Error: " + str(e)

def download_video(youtube_link, save_path):
    try:
        yt = YouTube(youtube_link)
        video = yt.streams.first()
        out_file = video.download(save_path)

        return "Video download 완료: " + out_file

    except Exception as e:
        return "Error: " + str(e)