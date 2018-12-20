# 라즈베리에서 실행

import gsm_weather
import Adafruit_CharLCD
import RPI.GPIO

# 날씨정보에서 카테고리에 관한 결과 코드 전달
def get_result_code(ctgory : str) -> str:
    weather_dict = get_weather_info(key)["response"]["body"]["items"]["item"]
    
    for i in weather_dict:
        if i["category"] == ctgory:
            return i["fcstValue"]

def sky_str(sky):
    if sky == 1:
        return "Sunny" # 맑음
    elif sky == 2:
        return "Cloudy" # 구름조금
    elif sky == 3:
        return "Cloud" # 구름많이
    else:
        return "Blur" # 흐림

def pty_str(pty):
    if pty == 0:
        return "None" # 없음
    elif pty == 1:
        return "Rainy" # 비
    elif pty == 2:
        return "Sleet" # 진눈깨비
    else:
        return "Snowy" # 눈

if __name__ == "__main__":
    lcd = Adafruit_CharLCD(rs = 22, en = 11, d4 = 23, d5 = 10, d6 = 9, d7 = 25, cols = 16, lines = 2)

    # sky : 날씨상태, pty : 강수상태
    sky, pty = get_result_code("SKY"), get_result_code("PTY")

    sky = sky_str(sky)
    pty = pty_str(pty)

    lcd.message("Weather : " + sky + "\n") # 날씨상태
    lcd.message("PPTN type : " + pty) # 강수형태
