import pyaudio


class MicrophoneListenerClass:
    
    @staticmethod
    def audio_stream_generator():
        # Define the parameters for the audio stream
        FORMAT = pyaudio.paInt16  # 16-bit format
        CHANNELS = 1  # Mono audio
        RATE = 16000  # 16kHz sample rate
        FRAME_DURATION_MS = 80  # Frame duration in ms
        FRAME_SIZE = int(RATE * FRAME_DURATION_MS / 1000)  # Calculate frame size

        # Initialize PyAudio
        audio = pyaudio.PyAudio()

        # Open the audio stream
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAME_SIZE
        )

        print(f"Streaming audio in frames of {FRAME_DURATION_MS} ms...")

        try:
            while True:
                # Read an audio frame
                audio_frame = stream.read(FRAME_SIZE)
                # Yield the audio frame to the calling context
                yield audio_frame
        finally:
            # Ensure the stream is stopped and closed properly even if an error occurs or the generator is stopped
            stream.stop_stream()
            stream.close()
            audio.terminate()
    
    def __init__(self) -> None:
        # for frame in MicrophoneListener.audio_stream_generator():
        #     print(f"Captured audio frame of length: {len(frame)} bytes")
        pass
        
if __name__ == "__main__":
    for frame in MicrophoneListenerClass.audio_stream_generator():
        print(f"Captured audio frame of length: {len(frame)} bytes")
    
    
