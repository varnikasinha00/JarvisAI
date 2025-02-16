from groq import Groq
from json import load,dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
client = Groq( api_key = GroqAPIKey )
messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advance AI chatbot named {Assistantname} which also have realtime up-to-date information of internet.
*** Do not tell time until i ask, do not talk too much, just answer to the question.***
*** Reply in the only english, even if the question is in hindi, reply in english.***
*** Do not provide note in the output, just answer the question and never mention your training data. ***"""

SystemChatBot = [
    {"role": "system",
    "content": System}]

try:

    with open(r"Data\ChatLog.json","r") as f:
        messages = load(f)

except:

    with open(r"Data\ChatLog.json","w") as f:
        dump([],f)

def RealtimeInformation():

    data=""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data+=f"Please use this realtime information if needed,\n"
    data+=f"Day: {day}\n"
    data+=f"Date: {date}\n"
    data+=f"Month: {month}\n"
    data+=f"Year: {year}\n"
    data+=f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

def AnswerModifier(Answer):

    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def ChatBot(Query):

    """ This function will send the query to the Chatbot and return the answer. """

    try:
        with open(r"Data\ChatLog.json","r") as f:
            messages:dict = load(f)
            
        messages.append({"role": "user", "content": f"{Query}"})
        completion = client.chat.completions.create(
        model = "llama3-70b-8192",
        messages = SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None)

        Answer =""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json","w") as f:
            dump(messages,f,indent=4)
        return AnswerModifier(Answer=Answer)
    
    except:
        with open(r"Data\ChatLog.json","w") as f:
            dump([],f,indent=4)
        return ChatBot(Query)

if __name__ == "__main__":

    while True:
        
        print(ChatBot(input("Enter Your Question : ")))

