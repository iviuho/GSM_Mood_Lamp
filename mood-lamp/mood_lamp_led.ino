#include <Adafruit_NeoPixel.h>
#include <Adafruit_WS2801.h>
#include <SPI.h>
#ifdef __AVR_ATtiny85__
#include <avr/power.h>
#endif
uint8_t dataPin  = 2; //yellow
uint8_t clockPin = 3; //green

Adafruit_WS2801 strip = Adafruit_WS2801(20, dataPin, clockPin);

void setup() {
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000L)
  clock_prescale_set(clock_div_1); //clock을 16Mhz로 사용
#endif

  strip.begin();

  //LEDstrip loop를 실행시키기 위해 모든 LED를 off시키며 초기화
  strip.show();
  Serial.begin(9600); //통신속도
  Serial.flush();
}


void loop() {
  String input=""; // 시리얼 통신으로 문자를 입력하기 위한 준비 
  while (Serial.available() > 0)// 시리얼 입력이 있을때
    {
        input += (char) Serial.read(); // 한번에 한문자를 읽으면
        delay(5); // 5밀리초 동안 대기하고 다음 문자를 읽을 준비
    }
  //입력한 패턴대로 LEDstrip를 실행
  if (input == "Sunny!"){  //아주맑음
    cc(Color(255, 70, 0), 1);
    }
  if (input == "Sunny."){  //맑음
    
    for (int i = 0; i < 127; i ++){
      cc(Color(i * 2, i, 0), 1);
    }
    
    for (int i = 127; i > 0; i--){
      cc(Color(i * 2, i, 0), 1);
    }
  
    }
  if (input == "Cloudy!"){  //아주흐림
    cc(Color(0, 0, 255), 1);
    }
  if (input == "Cloudy."){  //흐림
    a2();
    }
  if (input == "Rainy"){  //비
    a3();
    }
  if (input == "Sleet"){  //안개
    cc(Color(128, 128, 128), 1);
    }
  if (input == "Snowy"){  //눈
    a4();
    }
  if (input == "off"){
    cc(Color(0,0,0), 1);
    }
  }

/*void a1(){
 uint16_t i, j;
  for(j=0; j<256*2; j+=1){
    for(i=0; i<strip.numPixels(); i++) {
      int sum=i+j;
      map(sum,0,300,120,190);
      strip.setPixelColor(i, Wheel(sum),Wheel(sum) / 2,0); 
    }    
   strip.show();
   delay(10); 
  }
  
}*/

void a2(){
  uint16_t i, j;
  while(1){
  for(j=0; j<256*2; j+=1){
    for(i=0; i<strip.numPixels(); i++) {
      int sum=i+j;
      map(sum,0,300,120,190);
      strip.setPixelColor(i, 0, 0, Wheel(sum));
    }
    strip.show();
   delay(10); 
  }
  if(delay==5000)
    break;
  }
  return 0;
}

void a3(){
  uint16_t i ,j, k;
  while(1){
  for(k=0; k<2; k++)
    for(j=0; j<256; j+=1){
      for(i=0; i<strip.numPixels(); i++) {
        int sum=i+j;
        map(sum,0,300,120,190);
        strip.setPixelColor(i, Wheel(sum)-180, Wheel(sum)-180, Wheel(sum)-180);
      }
      strip.show();
     delay(10); 
    }
    if(delay==5000)
      break;
  }
  return 0;
}

void a4(){
  uint16_t i, j;
  while(1){
  for(j=0; j<256*2; j+=1){
    for(i=0; i<strip.numPixels(); i++) {
      int sum=i+j;
      map(sum,0,300,120,190);
      strip.setPixelColor(i, Wheel(sum), Wheel(sum), Wheel(sum));
    }
   strip.show();
   delay(10); 
  }
  if(delay==5000)
    break;
  }
  return 0;
}
//LED pixel을 입력한 색으로 차례대로 출력
void cc(uint32_t c, uint8_t wait) {
  int i;
  
  for (i=0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.show();
  }
  delay(wait);
}

//8비트의 r값 g값 b값을 받아서 여러가지의 색을 만드는 함수
uint32_t Color(byte r, byte g, byte b)
{
  uint32_t c;
  c = r;
  c <<= 8;
  c |= g;
  c <<= 8;
  c |= b;
  return c;
}   

//256이하의 숫자를 받았을 때 정해진 조건에 따라 특정색깔로 분리하여 나타내는 함수 
uint32_t Wheel(byte WheelPos)
{
  if (WheelPos < 85) {
   return Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if (WheelPos < 170) {
   WheelPos -= 85;
   return Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170; 
   return Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}
