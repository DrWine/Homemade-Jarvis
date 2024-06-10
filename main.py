from modules import LLmModule, WakeUpWord, WebSojet, stt, tts
import time
# Constants
API_KEY = 'OPENAI KEY'
LANGUAGES = ['ro-RO', 'ru-RU', 'en-EN']
OPENAI_VOICES = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
TTS_ENGINES = ['GTTS', 'OPENAI']

# Default settings
is_mic_on = True
language_index = 1
voices_index = 0
tts_engine = 0
temp_last_message = '\0'


## making the instances global...
s2t_instance = '\0'
wwd_instance = '\0'
gpt_instance = '\0'
tts_instance = '\0'

def get_bool_from_param(initial_state: bool, param: str, text: str) -> bool:
    """
    Extract a boolean value from a parameter in the text.
    
    Args:
        initial_state (bool): The default boolean value if the parameter is not found.
        param (str): The parameter to search for.
        text (str): The text to search within.

    Returns:
        bool: The extracted boolean value.
    """
    if param not in text:
        return initial_state

    index = text.find(param) + len(param)
    return text[index] == '1'

def get_int_from_param(initial_state: int, param: str, text: str) -> int:
    """
    Extract an integer value from a parameter in the text.

    Args:
        initial_state (int): The default integer value if the parameter is not found.
        param (str): The parameter to search for.
        text (str): The text to search within.

    Returns:
        int: The extracted integer value.
    """
    if param not in text:
        return initial_state

    index = text.find(param) + len(param)
    return int(text[index])

def instaces_builder():
    global wwd_instance, s2t_instance, gpt_instance, tts_instance
    global language_index, voices_index, tts_engine
    
    print(LANGUAGES[language_index], TTS_ENGINES[tts_engine], OPENAI_VOICES[voices_index])
    
    wwd_instance = WakeUpWord.WWD()
    
    s2t_instance = stt.VoiceRecognizer(
        WWD_instance=wwd_instance
        )
    
    gpt_instance = LLmModule.Gpt(
        language=LANGUAGES[language_index], api_key=API_KEY
        )
    
    tts_instance = tts.RealtimeTTS(
        language=LANGUAGES[language_index],
        api_key=API_KEY,
        the_engine=TTS_ENGINES[tts_engine],
        voice=OPENAI_VOICES[voices_index]
    )

if __name__ == '__main__':
    websocket_instance = WebSojet.WebSocket()

    try:
        while True:
            last_message = websocket_instance.get_last_message()
    
            if last_message != temp_last_message:
                print('\nSETTINGS REFRESH!!\n', last_message)
                
                is_mic_on = get_bool_from_param(is_mic_on, 'Mic', last_message)
                language_index = get_int_from_param(language_index, 'Language', last_message)
                voices_index = get_int_from_param(language_index, 'TTS_Voice', last_message)
                tts_engine = get_int_from_param(language_index, 'TTS', last_message)

                # REFRESHING THE MAIN INSTANCES
                instaces_builder()
                # Loop checker so we dont refresh instances every loop
                time.sleep(0.05)
                temp_last_message = last_message
    

            # Recognize speech and generate a response
            prompt = s2t_instance.recognize_speech(IsMicOn=is_mic_on, language=LANGUAGES[language_index])
            if not prompt:
                continue
            
            response = gpt_instance.chat_completion(prompt)
            
            ## ChatGpt Stream mode
            tts_instance.feed(response)
            tts_instance.play()
            print(response)
            
    except KeyboardInterrupt:
        print('Program terminated unexpectedly')
    
        
    
