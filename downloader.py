from pytube import YouTube
from moviepy.editor import *

def download_audio(yt, save_path):
    try:
        video = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        out_file = video.download(save_path)

        audio = AudioFileClip(out_file)
        audio.close()

        # Rename the file to .mp3
        base = os.path.splitext(out_file)[0]
        os.rename(out_file, base + '.mp3')

        return "완료"

    except Exception as e:
        print("에러: " + str(e))
        return "Error: " + str(e)

def download_video(yt, save_path):
    try:
        video = yt.streams.get_highest_resolution()
        out_file = video.download(save_path)

        return "완료"

    except Exception as e:
        print("에러: " + str(e))
        return "Error: " + str(e)


    

#download_audio("https://www.youtube.com/watch?v=mI-fTqb59Ss", "C:/Users/akshw/바탕 화면/test")