import Adafruit_CharLCD as LCD
import serial

import gsm_weather

# 하늘상태(SKY) 코드 : 맑음(1), 구름낀(2, 3), 흐림(4)
# 강수형태(PTY) 코드 : 없음(0), 비(1), 진눈깨비(2), 눈(3)
# 3시간 기온(T3H) 코드 : 단위 ℃

def get_weather_status(weather: dict) -> str:
    """하늘상태와 강수형태 값을 받고 해석해서 이에 해당하는 날씨 정보를 반환한다.

    매개 변수
    ----------
    weather: dict
        날씨 정보를 포함하고 있는 딕셔너리

    리턴
    -------
    str
        해석한 날씨 정보를 반환
    """
    pty_list = [None, "Rainy", "Sleet", "Snowy"]
    sky_list = [None, "Sunny!", "Sunny.", "Cloudy.", "Cloudy!"]

    if weather:
        pty, sky = weather["PTY"], weather["SKY"]
    else:
        pty, sky = 0, 0

    # 강수형태가 없음(0)이면 하늘상태 반환, 비나 눈이 오는 상황에는 강수형태 반환
    return pty_list[pty] if pty else sky_list[sky]

def init() -> object:
    """라즈베리파이 LCD의 초기 설정을 한다.

    리턴
    -------
    Adafruit_CharLCD.Adafruit_CharLCD
        핀 번호가 모두 지정되어 있는 LCD 객체
    """
    # 라즈베리파이 초기 설정   
    lcd_rs = 25
    lcd_en = 24
    lcd_d4 = 23
    lcd_d5 = 17
    lcd_d6 = 18
    lcd_d7 = 22
    lcd_backlight = 2

    # 16x2 사이즈로 행과 열을 설정
    lcd_columns = 16
    lcd_rows = 2
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

    return lcd

def set_message(weather: dict, lcd: object) -> bool:
    """라즈베리파이 LCD화면에 정보를 띄운다.

    매개 변수
    ----------
    weather: dict
        날씨 정보

    lcd: Adafruit_CharLCD.Adafruit_CharLCD
        LCD 객체
    """
    lcd.clear()
    
    if weather:
        status = get_weather_status(weather)
        
        lcd.message("Weather : %s\n" % status)
        lcd.message("Temperature : %s" % weather["T3H"])
        return True
    else:
        lcd.message("Can't get info!")
        return False

# Weather Case
# -> "Rainy", "Sleet", "Snowy", "Sunny!", "Sunny.", "Cloudy.", "Cloudy!"
    
def send_weather_status(msg: str):
    """시리얼 통신을 통해 아두이노로 메시지를 보낸다.

    매개 변수
    ----------
    msg: str
        시리얼 통신으로 보낼 메시지

    리턴
    -------
    int
        시리얼 통신을 통해 보낸 문자열의 바이트 수
    """
    for i in range(4):
        try:
            arduino = serial.Serial("/dev/ttyACM%s" % i)
            break
        except serial.serialutil.SerialException:
            pass
        
    if msg:
        return arduino.write(msg.encode())
    else:
        return 0

# 이 파일을 직접 실행해야 작동되는 부분
if __name__ == "__main__":
    key = ""
    lcd = init()
    set_message(gsm_weather.get_weather_info(key), lcd)
