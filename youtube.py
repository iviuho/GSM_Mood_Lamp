import youtube_dl

def download(url: str) -> bool:
    """유튜브에서 영상을 다운로드 후, MP3 파일을 추출한다.

    매개 변수
    ----------
    url: str
        다운로드 받을 유튜브의 링크

    리턴
    -------
    bool
        MP3 파일 저장에 성공했다면 True, 실패했다면 False
    """
    
    options = {
        "format" : "bestaudio/best",
        "extractaudio" : True,
        "audioformat" : "mp3",
        "outtmpl" : "%(title)s.%(ext)s",
        "noplaylist" : True,
        "nocheckcertificate" : True,
        "ignoreerrors" : False,
        "logtostderr" : False,
        "quiet" : True,
        "no_warnings" : True,
        "postprocessors" : [{
            "key" : "FFmpegExtractAudio",
            "preferredcodec" : "mp3",
            "preferredquality" : "192",
        }]
    }
    
    try:
        with youtube_dl.YoutubeDL(options) as ytdl:
            fileInfo = ytdl.extract_info(url, download = False)
            ytdl.download([url])
        return True
    except:
        return False

if __name__ == "__main__":
    pass
