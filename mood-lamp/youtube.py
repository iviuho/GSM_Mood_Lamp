import threading
import time

import pafy
import youtube_dl
import vlc

class Waiting_Item:
    def __init__(self, url: str):
        self.url = url
        self.pafy = pafy.new(url)
        self.name = self.pafy.title
        self.length = self.pafy.length
        self.file = None
        self.downloaded = False

    def download(self) -> bool:
        """유튜브에서 영상을 다운로드 후, MP3 파일을 추출한다.

        리턴
        -------
        bool
            MP3 파일 저장에 성공했다면 True, 실패했다면 False
        """
        import wget
        
        try:
            stream = self.pafy.getbestaudio()
            self.file = wget.download(stream.url, "%s.wav" % self.name)
            self.downloaded = True
        except FileNotFoundError:
            self.file = wget.download(stream.url, "%s.wav" % self.replace_name())
            self.downloaded = True
        except:
            return False
        else:
            return True

    def replace_name(self) -> str:
        """파일 이름 지정 규칙에 따라서 파일 이름을 수정한 후 리턴한다.

        리턴
        -------
        str
            파일 이름 규칙을 준수하는 문자열
        """
        import re

        res = set(re.compile("[^[\w[\`\'\˜\=\+\#\ˆ\@\$\&\-\_\.\(\)\{\}\;\[\] ]").findall(self.name))
        new_name = self.name
        for i in res:
            new_name = new_name.replace(i, "")
        return new_name

class Download_Queue(list):
    def enqueue(self, item: Waiting_Item):
        self.append(item)
        threading.Thread(target = item.download, daemon = True).start()

    def dequeue(self):
        return self.pop(0)

    def is_empty(self):
        return not len(self) > 0

class Player:
    def __init__(self):
        self.__playing = False
        self.queue = Download_Queue()
        self.player = vlc.MediaPlayer()

    def play(self): # 표면적인 재생을 맡는 함수
        if self.__playing:
            pass
            # print("이미 노래가 재생 중 입니다.")
        else:
            self.thread = threading.Thread(target = self.__play, daemon = True)
            self.thread.start()

    def __play(self): # 실질적인 재생을 맡는 함수
        # 큐에 있는 곡 전부 다 없어질 때까지 반복
        import os
        
        while not self.queue.is_empty():
            item = self.queue.dequeue()
            if item.downloaded:
                print("%s 재생을 시작합니다." % item.name)
                self.player.set_media(vlc.Media(item.file))
                self.player.play()
                time.sleep(item.length)
                self.player.stop()
                os.remove(item.file)
            else:
                for i in range(5):
                    print("%s 다운로드에 실패했습니다." % item.name)
                    print("남은 재시도 횟수 : %s" % (5 - i))
                    time.sleep(5)
                    if item.downloaded:
                        self.queue.insert(0, item)
                        break
                else:
                    self.queue.append(item)
                    print("%s 노래를 건너뜁니다." % item.name)
        print("대기열에 재생할 곡이 더 이상 없습니다.")   
        self.__playing = False

    def add(self, keyword: str):
        self.queue.enqueue(get_item(keyword))

def find_video(keyword: str) -> str:
    """유튜브에서 찾고 싶은 키워드를 입력받고, 그 동영상의 URL를 돌려줍니다.

    매개 변수
    ----------
    keyword: str
        찾고 싶은 키워드

    리턴
    -------
    str
        검색 완료된 영상의 URL
    """
    import youtube_dl
    
    options = {
        "format" : "bestaudio/best",
        "extractaudio" : True,
        "audioformat" : "mp3",
        "outtmpl" : "%(title)s.%(ext)s",
        "noplaylist" : True,
        "nocheckcertificate" : True,
        "ignoreerrors" : True,
        "logtostderr" : False,
        "quiet" : True,
        "no_warnings" : True
    }

    with youtube_dl.YoutubeDL(options) as ytdl:
        return ytdl.extract_info("ytsearch1:%s" % keyword, download = False)["entries"][0]["webpage_url"]

def get_item(keyword: str) -> Waiting_Item:
    return Waiting_Item(find_video(keyword))

if __name__ == "__main__":
    """
    player = Player()
    player.add("something")
    player.add("something2")
    player.play()
    
    player.thread.join()
    """
