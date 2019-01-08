from __future__ import division

import re
import sys
import time
import threading

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.api_core.exceptions import OutOfRange
import pyaudio
from six.moves import queue

import gsm_weather
import music_search
import lamp
from youtube import Player
from command import Command_Manager

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format = pyaudio.paInt16,
            channels = 1, rate = self._rate,
            input = True, frames_per_buffer = self._chunk,
            stream_callback = self._fill_buffer,
        )
        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block = False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)
 
def main(player: object, manager: object):
    """전체 프로그램을 돌리기 위한 메인 함수.

    매개 변수
    ----------
    player: object
        youtube.Player 객체

    manager: object
        command.Command_Manager 객체
    """
    language_code = "ko-KR"  # 한국어로 변경

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = RATE,
        language_code = language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config = config,
        interim_results = True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content = content) for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        for i in responses:
            if not i.results or not i.results[0].alternatives or not i.results[0].is_final:
                continue

            transcript = i.results[0].alternatives[0].transcript
            print(transcript)

            if not manager.is_command(transcript):
                continue

            command = manager.get_command(transcript)

            if not command:
                continue
            elif command == "play":
                melon_result = music_search.search_music("".join(transcript.split()[:-1]))
                print(melon_result)

                artist, title = melon_result
                if not melon_result == (None, None):
                    player.add("%s - %s" % (artist, title))
                    player.play()
            elif command == "pause":
                player.pause()
            elif command == "resume":
                player.resume()
            elif command == "skip":
                player.skip()
            else:
                lamp.send_weather_status(command)

def run_lamp(key: str):
    weather = gsm_weather.get_weather_info(key)

    while True:
        msg = "Weather: %s" % lamp.get_weather_status(weather)
        msg += "Temperature: %s" % weather["T3H"]
        print(msg)

        # LCD에 텍스트 표시
        lcd = lamp.init()
        lamp.set_message(weather, lcd)

        # LED 색깔 바꾸기 위해 시리얼 통신
        # lamp.send_weather_status(lamp.get_weather_status(weather))
        time.sleep(10800) # 3시간 = 3 * 60 * 60초
        
if __name__ == "__main__":
    key = "pyoHDO8lB68iVD2hCcD32nZNaD%2FDpgW2bQUA%2FnQKpwfJVv%2BUncuibmJHIEX7lIoj%2BNd6VTZ7JKMQF%2FLM5%2FVX%2Bg%3D%3D"

    lamp_thread = threading.Thread(target = run_lamp, args = (key, ), daemon = True)
    lamp_thread.start()

    player = Player()
    manager = Command_Manager("command.txt")

    while True:
        try:
            main(player, manager)
        except OutOfRange:
            pass
        except KeyboardInterrupt:
            break
