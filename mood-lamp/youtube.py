import youtube_dl
import threading
import pafy
import time

class Waiting_Item:
    def __init__(self, url):
        self.url = url
        self.name = None
        self.length = pafy.new(url).length
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
            self.name = fileInfo["title"]
            return True
        except:
            return False

    def check_length(self, url) -> int:
        video = pafy.new(url)

        # video.duration : 영상 길이가 00:05:47 형식으로 나온다.
        dur = video.duration.split(':')
        dur = [int(i) for i in dur] # dur = map(int, dur)

        for i in range(2):
            dur[i + 1] += dur[i] * 60 
            dur[i] = 0
        return dur[2] # 영상의 초를 반환한다.

class Download_Queue(list):
    def enqueue(self, item: Waiting_Item):
        self.append(item)

    def dequeue(self):
        return self.pop(0)

    def is_empty(self):
        return not len(self) > 0

    def play(self):
        if self.is_empty():
            print("대기열에 재생할 곡이 없습니다.")
            return
        else:
            item = self.dequeue()
            # 물품 도착 후 세부 구현 예정
            if item.download():
                print("%s 재생을 시작합니다." % item.name)
            else:
                print("%s 다운로드에 실패했습니다." % item.name)
            # 물품 도착 후 세부 구현 예정

    def play_end(self): # 큐에 있는곡 전부다 없어질 때까지 반복
        while not self.is_empty():
            item = self.dequeue()
            if item.download():
                print("%s 재생을 시작합니다." % item.name)
                # time.sleep(item.length)
            else:
                print("%s 다운로드에 실패했습니다." % item.name)
        print("대기열에 재생할 곡이 더이상 없습니다.")

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

def get_item(keywd : str):
    url = find_video(keywd)
    item = Waiting_Item(url)
    return item


def music_play(queue : object):
    queue.play_end()

if __name__ == "__main__":
    queue = Download_Queue()

    # button.wait_for_press() # 버튼을 누를때까지 기다림(라즈베리에서 실행)
    
    keywd = "삐삐" # 음성인식한 키워드
    queue.enqueue(get_item(keywd))
    
    try:    
        t1 = threading.Thread(target = music_play, args = (queue, ))
        t1.start()
    except Exception as e:
        print(e)

    while queue.is_empty():
        print("while문") 
        if True: # 버튼을 누를시 
            keywd = "야생화" # 음성인식한 키워드
            queue.enqueue(get_item(keywd))
        
    print("종료")
        
