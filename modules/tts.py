from RealtimeTTS import TextToAudioStream, OpenAIEngine, GTTSEngine

class RealtimeTTS:
    def __init__(self, api_key, language='ru-RU', the_engine='GTTS', voice = 'alloy') -> None:
        self.api_key = api_key

        if the_engine == 'GTTS':
            self.engine = GTTSEngine(voice=language[:2])

        if the_engine == 'OPENAI':
            self.engine = OpenAIEngine('tts-1', voice)

        self.stream = TextToAudioStream(self.engine, language=language)

    def feed(self, text):
        print(f"Feeding text: {text}")
        self.stream.feed(text)

    def play(self):
        try:
            print("Attempting to play...")
            self.stream.play()
        except Exception as e:
            print(f"An error occurred in play(): {e}")
            raise

if __name__ == '__main__':
    api_key = 'OPENAI KEY'
    tts = RealtimeTTS(language='ro-RO', the_engine='OPENAI', api_key=api_key)
    tts.feed("Salut, Ce mai faci?!")
    tts.play()
