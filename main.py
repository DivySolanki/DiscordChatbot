# app id = 1193920102555455498
# public key = 65b49fbc00475f89eed93295eba61799294f95a6a4fff88601c0a81b2b28c5e3
import discord
import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()

with open('chat.txt', 'r') as f:
    chat = f.read()
chat = ""

TOKEN = os.environ['SECRET_KEY']
OPENAI_KEY = os.environ['OPENAI_KEY']

openai = OpenAI(api_key=OPENAI_KEY)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        chat += f"{message.author}: {message.content}\n"
        print(f'Message from {message.author}: {message.content}')
        if self.user != message.author:
            if self.user in message.mentions:
                response = openai.completions.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=f"{chat}\nSaviorBot: ",
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                messageToSend = response.choices[0].text
                channel = message.channel
                await channel.send(messageToSend)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
