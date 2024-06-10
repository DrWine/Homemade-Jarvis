history = [
            {"role": "system", "content": "You are an assistant, your name is Jarvis, you do what you're asked. You don't ask any questions. At the end of the speech you say ', sir.' SPEAK IN RUS. iată mesajul utilizatorului: "},
               ]
history.append({"role": "user", "content": 'message'})

print(history)
history.append({"role": "user", "content": 'message2'})