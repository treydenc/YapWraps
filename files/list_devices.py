import sounddevice as sd

devices = sd.query_devices()

for idx, device in enumerate(devices):
    print(f"{idx}: {device['name']}")
    print(f"   Max Input Channels: {device['max_input_channels']}")
    print(f"   Max Output Channels: {device['max_output_channels']}")
