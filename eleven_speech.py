import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import time
from openai import OpenAI
from pydub import AudioSegment
import RPi.GPIO as GPIO
import pygame
from elevenlabs import ElevenLabs, VoiceSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# Check if API keys are available
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

if not ELEVENLABS_API_KEY:
    raise ValueError("Eleven Labs API key not found. Please set it in the .env file.")

# Initialize API clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Constants and configurations
BUTTON_PIN = 16  # GPIO pin number where the button is connected
input_device_index = 1  # Replace with your microphone's device index
output_device_index = 2  # Replace with your speaker's device index
audio_filename = 'recorded_audio.wav'
speech_filename = 'polite_audio.mp3'

# Set up GPIO for button input
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global variable to disable button during processing
button_enabled = True

# Step 1: Record audio from microphone
def record_audio(filename, input_device_index):
    print("Recording...")
    fs = 48000  # Sample rate
    channels = 1  # Mono recording
    recorded_data = []

    start_time = time.time()
    min_duration = 3  # Minimum recording time in seconds

    # Start recording
    with sd.InputStream(samplerate=fs, channels=channels, dtype='int16', device=input_device_index) as stream:
        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                data, _ = stream.read(1024)
                recorded_data.append(data)
            else:
                # Check if minimum recording duration is met
                if time.time() - start_time >= min_duration:
                    break
                else:
                    data, _ = stream.read(1024)
                    recorded_data.append(data)

    # Concatenate recorded data
    recorded_audio = np.concatenate(recorded_data, axis=0)

    # Save the recorded audio to a WAV file
    write(filename, fs, recorded_audio)
    print("Recording complete")

# Step 2: Transcribe audio using OpenAI Whisper API
def transcribe_audio(audio_filename):
    print("Transcribing audio...")
    with open(audio_filename, 'rb') as audio_file:
        transcription = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    transcription_text = transcription.text
    print("Transcription complete")
    print("Transcribed text:", transcription_text)
    return transcription_text

# Step 3: Rephrase text using OpenAI ChatGPT
def make_polite_text(transcribed_text):
    print("Generating polite text...")
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that rephrases polite text to dirty and raw truth. Use curse words and humor to reveal the emotional truth and desires behind polite language."
            },
            {
                "role": "user",
                "content": transcribed_text
            }
        ]
    )
    polite_text = response.choices[0].message.content.strip()
    print("Polite text generation complete")
    print("Polite text:", polite_text)
    return polite_text

# Step 4: eleven labs tts
def text_to_speech(polite_text, speech_filename):
    print("Generating speech from polite text using Eleven Labs TTS...")
    try:
        # Configure voice settings if needed
        voice_settings = VoiceSettings(
            stability=0.2,
            similarity_boost=0.9,
            style=0.4,
        )

        # Generate the speech audio as a generator
        audio_generator = eleven_client.text_to_speech.convert(
            voice_id="fxO7BD0lOiWADH5LwvFr",  # Replace with your desired voice ID
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",  # Adjust the output format if necessary
            text=polite_text,
            voice_settings=voice_settings,
	    model_id="eleven_turbo_v2_5",
        )

        # Save the audio to a file by writing each chunk
        with open(speech_filename, 'wb') as f:
            for chunk in audio_generator:
                if chunk:
                    f.write(chunk)
        print("Speech generation complete")
    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")

# Step 5: Play the audio file through USB speaker using pygame
def play_audio(speech_filename):
    print("Playing audio...")
    pygame.mixer.init()
    pygame.mixer.music.load(speech_filename)
    pygame.mixer.music.play()
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
    print("Audio playback complete")

def main():
    global button_enabled

    try:
        while True:
            # Wait for the button to be pressed
            if GPIO.input(BUTTON_PIN) == GPIO.LOW and button_enabled:
                button_enabled = False  # Disable button until processing is complete
                print("Button Pressed")
                record_audio(audio_filename, input_device_index)

                # Transcribe the recorded audio
                transcribed_text = transcribe_audio(audio_filename)

                # Rephrase the transcribed text
                polite_text = make_polite_text(transcribed_text)

                # Convert the polite text back to speech
                text_to_speech(polite_text, speech_filename)

                # Play the polite audio
                play_audio(speech_filename)

                # Re-enable the button after processing
                button_enabled = True
                print("Ready for next recording")

            time.sleep(0.1)  # Small delay to prevent CPU overuse

    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
