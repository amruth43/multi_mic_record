import pyaudio
import wave
import multiprocessing as mp

def usb_record(u_channel):
	USB_RATE = 44100
	USB_CHANNELS = u_channel #need 1 channels for USB
	USB_WIDTH = 2 # it refers to the number of bytes normally 2 is good 
	USB_INDEX = 4 # refer to input device id
	CHUNK = 1024
	RECORD_SECONDS = 10
	WAVE_OUTPUT_FILENAME = "MONO_USB_output.wav"
	
	p = pyaudio.PyAudio()
	
	stream = p.open(
		rate=USB_RATE,
		format=p.get_format_from_width(USB_WIDTH),
		channels=USB_CHANNELS,
		input=True,
		input_device_index=USB_INDEX,)
	
	print("* USB_MONO_recording")
	
	frames = [] 
	
	for i in range(0, int(USB_RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	
	print("* done_USB_MONO_recording")
	
	stream.stop_stream()
	stream.close()
	p.terminate()
	
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(USB_CHANNELS)
	wf.setsampwidth(p.get_sample_size(p.get_format_from_width(USB_WIDTH)))
	wf.setframerate(USB_RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


def respeaker6pi_record(r_channels):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS =  r_channels
	RATE = 16000
	RECORD_SECONDS = 10
	WAVE_OUTPUT_FILENAME = "RESPEAKER_6_PI_output.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
		        channels=CHANNELS,
		        rate=RATE,
		        input=True,
		        frames_per_buffer=CHUNK)

	print("* RESPEAKER_6_PI_recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	print("* done _RESPEAKER_6_PI_recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


p_usb = mp.Process(target = usb_record, args=(1,))
p_rs = mp.Process(target =  respeaker6pi_record,  args=(8,))


p_usb.start()
p_rs.start()

p_usb.join()	# wait until process p_usb complete
p_rs.join() 	# wait until process p_rs complete


