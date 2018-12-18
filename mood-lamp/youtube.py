import youtube_dl

class WaitingItem:
    def __init__(self, url):
        self.url = url
        self.options = {
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

    def download(self) -> bool:
        """유튜브에서 영상을 다운로드 후, MP3 파일을 추출한다.

        리턴
        -------
        bool
            MP3 파일 저장에 성공했다면 True, 실패했다면 False
        """
        try:
            with youtube_dl.YoutubeDL(self.options) as ytdl:
                fileInfo = ytdl.extract_info(self.url, download = False)
                ytdl.download([self.url])
            return True
        except:
            return False

if __name__ == "__main__":
    pass
