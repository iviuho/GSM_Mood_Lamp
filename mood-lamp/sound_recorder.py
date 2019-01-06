# https://gist.github.com/mabdrabo/8678538

import pyaudio
import wave
 
def sound_recorder():
	FORMAT = pyaudio.paInt16
	CHANNELS = 1  #only mono
	RATE = 16000  
	CHUNK = 1024  #확인 필요
	RECORD_SECONDS = 5 #5초 녹음

	WAVE_OUTPUT_FILENAME = "file.wav"
	 
	audio = pyaudio.PyAudio()
	 
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
	                rate=RATE, input=True,
	                frames_per_buffer=CHUNK)
	print ("recording...")
	frames = []
	 
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	print ("finished recording")
	 
	 
	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	 
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

	return data

if __name__ == "__main__" :
	print("data : %s" % sound_recorder())
