import speech_recognition as sr

class VoiceRecognizer:
    def __init__(self, WWD_instance):
        self.wwd_instance = WWD_instance
        
        if WWD_instance == None:
            raise ValueError('WWD_instance == null')
        
        self.history = []
        self.prompt = ""
        self.call_count = 0
    
    def reset_history(self):
        self.history = []
        self.call_count = 0
    
    def recognize_speech(self, IsMicOn = True, language = 'ru=RU'):
        
        if IsMicOn == False:
            return False
        
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        if self.wwd_instance.is_awaken():
                
            self.call_count += 1
            if self.prompt:
                self.history.append(self.prompt)
                self.prompt = ""
                
            if self.call_count >= 11:
                self.reset_history()
                    
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                try:
                    audio = recognizer.listen(source, timeout=4)
                    print("Recognizing...")
                    self.prompt = recognizer.recognize_google(audio, language=language)
                    print(f"Recognized: {self.prompt}")
                    return self.prompt
                    
                except sr.WaitTimeoutError:
                    print("No speech detected in 4 seconds.")
                    return False
                    
                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                    return False
                    
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    return False
                    

            # else:
            #     time.sleep(1)  # Wait for a second before checking again

    def get_prompt(self):
        return self.prompt
    
if __name__ == '__main__':
    # Utilizare
    voice_recognizer = VoiceRecognizer()
    voice_recognizer.recognize_speech()
