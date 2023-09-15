import discord
from discord.ext import commands
import os
import openai
import asyncio

token = "YOUR_BOT_TOKEN"
os.environ['TOKEN'] = token

openai_apikey = "OPENAI_API_KEY"
os.environ['OPENAI_API_KEY'] = openai_apikey

from langchain.prompts import (
  ChatPromptTemplate, 
  MessagesPlaceholder, 
  SystemMessagePromptTemplate, 
  HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

token = os.environ['TOKEN']
openai.api_key = os.environ['OPENAI_API_KEY']

system_settings = """あなたはWeb3やIT技術に詳しいアシスタント型AIです。""" #AI characteristics can be changed arbitrarily
prompt = ChatPromptTemplate.from_messages([
  SystemMessagePromptTemplate.from_template(system_settings),
  MessagesPlaceholder(variable_name="history"),
  HumanMessagePromptTemplate.from_template("{input}")
])

use_model = "gpt-3.5-turbo" #GPT version can also be changed arbitrarily
S_conversation = ConversationChain(
  memory=ConversationSummaryBufferMemory(
    return_messages=True,
    llm=ChatOpenAI(model_name=use_model),
    max_token_limit=1000 #Number of characters a bot can send
  ),
  prompt=prompt,
  llm=ChatOpenAI(model_name=use_model),
  verbose=True
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="/",
    intents=intents
)  

@bot.event
async def on_ready():
    print(f'{bot.user}が正常に実行されました') #Bot startup log (terminal)

@bot.command()
async def ask(ctx, *, question):
    async with ctx.typing(): #Typing animation
        S_text = S_conversation.predict(input=question)
        await ctx.send(S_text)

        S_memory_text = S_conversation.memory.load_memory_variables({})
        Sf = open('memory.txt', 'w') #A log of the conversation is recorded in memory.txt (*If not created, it will be automatically added to the file)
        Sf.write(str(S_memory_text))
        Sf.close()

bot.run(token)