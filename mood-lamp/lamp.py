# 주석 친 코드는 라즈베리에서 실행

import gsm_weather
# import Adafruit_CharLCD
# import RPI.GPIO as GPIO

# 날씨정보에서 카테고리에 관한 결과 코드 전달
def get_result_data(weather: dict, category : str) -> int:
    """날씨 정보에서 입력받은 카테고리의 값을 반환해준다.

    매개 변수
    ----------
    weather: dict
        API에서 받아온 날씨 정보 딕셔너리를 넣는다.
    category: str
        딕셔너리에서 얻고 싶은 카테고리를 넣는다.

    리턴
    -------
    int
        해당 카테고리의 값을 반환한다.
    """
    for i in weather["response"]["body"]["items"]["item"]:
        if i["category"] == category:
            return i["fcstValue"]

def inform_sky_pty(sky: int, pty: int) -> str:
    """하늘상태와 강수형태 값을 받고 해석해서 이에 해당하는 날씨 정보를 반환한다.

    매개 변수
    ----------
    sky: int
        하늘상태
    pty: int
        강수형태

    리턴
    -------
    str
        해석한 날씨 정보를 반환
    """
    skylist = ["Sunny", "Cloudy", "Cloudy", "Blur"]
    ptylist = ["None", "Rainy", "Sleet", "Snowy"]
    
    if not pty: # 강수형태가 없음(0)이 아니면
        return skylist[sky - 1]
    return ptylist[pty]


# 하늘상태(SKY) 코드 : 맑음(1), 구름낀(2, 3), 흐림(4)
# 강수형태(PTY) 코드 : 없음(0), 비(1), 진눈깨비(2), 눈(3)
# 3시간 기온(T3H) 코드 : 단위 ℃

# 이 파일을 직접 실행해야 작동되는 부분
if __name__ == "__main__":
    # lcd = Adafruit_CharLCD(rs = 22, en = 11, d4 = 23, d5 = 10, d6 = 9, d7 = 25, cols = 16, lines = 2)
    # sky : 하늘상태, pty : 강수형태
    # lcd.message("Weather : " + weather_status + "\n") # 날씨 상태
    # lcd.message("Temperature : " + t3h) # 기온
 
