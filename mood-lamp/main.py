
import gsm_weather
import music_search
# import lamp
import speech

from youtube import Player
from command import Command_Manager
# from Thread import threading

def main():
	manager = Command_Manager("command.txt")
	player = Player()

	# lamp.set_message(gsm_weather.get_weather_info(key), lcd)

	while True:
		msg = speech.main()

		if manager.is_command(msg):
			tuple_data = music_search.serch_music(msg.split()[:-1])
			player.add("%s - %s" % (tuple_data[0], tuple_data[1]))
			player.play()

if __name__ == "__main__":
	main()
		
		
	