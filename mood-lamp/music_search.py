import requests
from bs4 import BeautifulSoup

def get_html(url):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"}
    return requests.get(url, headers = header).text

def search_music(music):
    """Melon 음악 사이트에서 검색을 해서 실존하는지 검사합니다.

    매개 변수
    ----------
    music: str
        검색을 원하는 검색어

    리턴
    -------
    tuple
        (노래 제목, 노래를 부른 가수)로 구성된 튜플, 검색 결과가 없다면 None을 반환한다.
    """
    try:
        melon_html = get_html("https://www.melon.com/search/total/index.htm?q=%s&section=&linkOrText=T&ipath=srch_form" % music)
        melon_parse = BeautifulSoup(melon_html, "html.parser")
        
        title = melon_parse.select("#frm_searchSong > div > table > tbody > tr:nth-of-type(1) > td:nth-of-type(3) > div > div > a.fc_gray")
        artist = melon_parse.select("#artistName > a")
        return (artist[0].text, title[0].text)
    except IndexError:
        return (None, None)

if __name__ == "__main__":
    pass
