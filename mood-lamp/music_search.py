import requests
from bs4 import BeautifulSoup




global header
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}


def search_music(music):
    try :
        melon = requests.get('https://www.melon.com/search/total/index.htm?q={0}&section=&linkOrText=T&ipath=srch_form'.format(music), headers = header)
        melon_html = melon.text
        melon_parse = BeautifulSoup(melon_html, 'html.parser')
        title = melon_parse.select('#frm_searchSong > div > table > tbody > tr:nth-of-type(1) > td:nth-of-type(3) > div > div > a.fc_gray')
        artist = melon_parse.select('#artistName > a')
        return artist[0].text,title[0].text
    except IndexError:
        return "노래가 없습니다"

if __name__ == "__main__":
    while 1:
        msg = input("입력 : ")
        print(search_music(msg))


    
#frm_searchSong > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > div > div > a.fc_gray
