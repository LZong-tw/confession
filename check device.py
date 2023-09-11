import speech_recognition as sr
import pyaudio

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize PyAudio
p = pyaudio.PyAudio()

# List available microphones
info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')
for i in range(0, num_devices):
    device_info = p.get_device_info_by_host_api_device_index(0, i)
    print(f"Device {i}: {device_info['name']}")

# Close PyAudio
p.terminate()
