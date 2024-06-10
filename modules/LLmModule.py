import os
from openai import OpenAI

class Gpt:
    def __init__(self, language="ru-RU", api_key='', engine='OpenAi', model='gpt-3.5-turbo') -> None:
        
        self.history = [
                    {"role": "system", "content": "You are an assistant, your name is Jarvis, you do what you're asked. You don't ask any questions. At the end of the speech you say ', sir.' SPEAK IN " + language + ". iată mesajul utilizatorului: "},
                ]
        
        self.api_key = api_key
        self.model = model
        
        if engine == 'Ollama':
            self.api_key = 'ollama'
            self.client = OpenAI(api_key=self.api_key, base_url='http://localhost:11434/v1/')
            return 
        
        #else engine == openai:
        os.environ["OPENAI_API_KEY"] = self.api_key
        self.client = OpenAI(api_key=self.api_key)
    
    def chat_completion(self, message):
        try:
            self.history.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                messages=self.history,
                model=self.model,
                max_tokens=300,
                temperature=0.7,
            )

            # Accessing the message content from the response
            completion = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": completion})
            return completion
        except Exception as e:
            print("Error:", e)
            return None


if __name__ == '__main__':
    api_key = 'OPENAI KEY'  # Replace with your actual API key
    gpt_instance = Gpt(language="ru-RU", api_key=api_key)
    while True:
        prompt = input('Write your prompt: ')
        response = gpt_instance.chat_completion(prompt)
        print(response)
