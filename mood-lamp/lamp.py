# 라즈베리에서 실행

import gsm_weather
import Adafruit_CharLCD
import RPI.GPIO as GPIO

# 날씨정보에서 카테고리에 관한 결과 코드 전달
def get_result_code(ctgory : str) -> str:
    weather_dict = get_weather_info(key)["response"]["body"]["items"]["item"]
    
    for i in weather_dict:
        if i["category"] == ctgory:
            return i["fcstValue"]

'''
def sky_str(sky):
    status_list = ["Sunny", "Cloudy", "Cloudy", "Blur"]
    return status_list[sky - 1]

def pty_str(pty):
    status_list = ["None", "Rainy", "Sleet", "Snowy"]
    return status_list[pty]
'''

def inform_sky_pty(sky, pty):
    skylist = ["Sunny", "Cloudy", "Cloudy", "Blur"]
    ptylist = ["None", "Rainy", "Sleet", "Snowy"]
    
    if pty != 0: # 강수형태가 없음(0)이 아니면
        return skylist[sky - 1]
    return ptylist[pty]


# 하늘상태(SKY) 코드 : 맑음(1), 구름낀(2, 3), 흐림(4)
# 강수형태(PTY) 코드 : 없음(0), 비(1), 진눈깨비(2), 눈(3)

# 이 파일을 직접 실행해야 작동되는 부분
if __name__ == "__main__":
    lcd = Adafruit_CharLCD(rs = 22, en = 11, d4 = 23, d5 = 10, d6 = 9, d7 = 25, cols = 16, lines = 2)

    # sky : 하늘상태, pty : 강수형태
    sky, pty = get_result_code("SKY"), get_result_code("PTY")
    t3h = get_result_code("T3H")

    weather_status = inform_sky_pty(sky, pty)

    lcd.message("Weather : " + weather_status + "\n") # 날씨 상태
    lcd.message("Temperature : " + t3h) # 기온
