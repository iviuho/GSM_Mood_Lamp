# import Adafruit_CharLCD
# import RPI.GPIO as GPIO

import gsm_weather

def get_weather_status(pty: int, sky: int) -> str:
    """하늘상태와 강수형태 값을 받고 해석해서 이에 해당하는 날씨 정보를 반환한다.

    매개 변수
    ----------
    pty: int
        강수형태
    sky: int
        하늘상태

    리턴
    -------
    str
        해석한 날씨 정보를 반환
    """
    pty_list = ["None", "Rainy", "Sleet", "Snowy"]
    sky_list = ["None", "Sunny!", "Sunny.", "Cloudy.", "Cloudy!"]

    # 강수형태가 없음(0)이면 하늘상태 반환, 비나 눈이 오는 상황에는 강수형태 반환
    return pty_list[pty] if pty else sky_list[sky]


# 하늘상태(SKY) 코드 : 맑음(1), 구름낀(2, 3), 흐림(4)
# 강수형태(PTY) 코드 : 없음(0), 비(1), 진눈깨비(2), 눈(3)
# 3시간 기온(T3H) 코드 : 단위 ℃

# 이 파일을 직접 실행해야 작동되는 부분
if __name__ == "__main__":
    key = ""
    weather = gsm_weather.get_weather_info(key)

    if weather:
        print("기준 시간 : %s" % weather["fcstTime"])
        print("Weather : %s\n" % get_weather_status(weather["PTY"], weather["SKY"]))
        print("Temperature : %s" % weather["T3H"])
    else:
        print("Can't get info!")
        
    # lcd = Adafruit_CharLCD(rs = 22, en = 11, d4 = 23, d5 = 10, d6 = 9, d7 = 25, cols = 16, lines = 2)
    # lcd.message
 
