import pyaudio
import wave

USB_RATE = 44100
USB_CHANNELS = 1 #need 8 channels
USB_WIDTH = 2
# run getDeviceInfo.py to get index
USB_INDEX = 2 # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(
	rate=USB_RATE,
	format=p.get_format_from_width(RESPEAKER_WIDTH),
	channels=USB_CHANNELS,
	input=True,
	input_device_index=RESPEAKER_INDEX,)

print("* recording")

frames = [] 

for i in range(0, int(USB_RATE / CHUNK * RECORD_SECONDS)):
	data = stream.read(CHUNK)
	frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(USB_CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(USB_WIDTH)))
wf.setframerate(USB_RATE)
wf.writeframes(b''.join(frames))
wf.close()
