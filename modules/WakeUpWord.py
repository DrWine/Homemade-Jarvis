import openwakeword
import keyboard
import numpy as np
from .MicrophoneListener import MicrophoneListenerClass
from openwakeword.model import Model
import threading

class WWD:
    def __init__(self) -> None:
        openwakeword.utils.download_models()
        keyboard.add_hotkey('num 0', self.on_shortcut)
        
        self.model = Model(
            wakeword_models=["alexa"],
        )
        self.is_called = False
        self.start_listening()

    def on_shortcut(self):
        self.is_called = True

    def start_listening(self):
        def listen():
            for frame in MicrophoneListenerClass.audio_stream_generator():
                prediction = self.model.predict(np.frombuffer(frame, dtype=np.int16))
                self.is_called = True if prediction['alexa'] > 0.9 else False

        listening_thread = threading.Thread(target=listen)
        listening_thread.daemon = True
        listening_thread.start()

    def is_awaken(self):
        return self.is_called

if __name__ == '__main__':
    wwd = WWD()
    while True:
        if wwd.is_awaken():
            print("Wake word detected")
