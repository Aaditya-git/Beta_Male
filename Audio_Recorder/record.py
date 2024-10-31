import wave
import struct
import time  

from pvrecorder import PvRecorder
from config import saved_audio_path

devices = PvRecorder.get_available_devices()
for index, device in enumerate(devices):
    print(f"Device {index}: {device}")

recorder = PvRecorder(device_index=0, frame_length=4096)  # (32 milliseconds of 16 kHz audio)
audio = []
path = saved_audio_path

try:
    recorder.start()
    
    start_time = time.time()  
    duration = 15  

    while True:
        frame = recorder.read()
        audio.extend(frame)

        
        if time.time() - start_time >= duration:
            print("Recording stopped after 15 seconds.")
            break  
except KeyboardInterrupt:
    recorder.stop()
    print("Recording interrupted by user.")
finally:
    recorder.stop() 
    with wave.open(path, 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))
    recorder.delete() 
