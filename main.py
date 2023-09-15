import discord
from discord.ext import commands
import os
import openai
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory

# Enter discord bot token and OpenAI KEY
os.environ['TOKEN'] = "YOUR_BOT_TOKEN"
os.environ['OPENAI_API_KEY'] = "OPENAI_API_KEY"

# Discord Bot Setting
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

openai.api_key = os.environ['OPENAI_API_KEY']
system_settings = """あなたはWeb3やIT技術に詳しいアシスタント型AIです。""" # Bot characteristics can be changed at will :)
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_settings),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
use_model = "gpt-3.5-turbo"
S_conversation = ConversationChain(
    memory=ConversationSummaryBufferMemory(
        return_messages=True,
        llm=ChatOpenAI(model_name=use_model),
        max_token_limit=1000
    ),
    prompt=prompt,
    llm=ChatOpenAI(model_name=use_model),
    verbose=True
)

# Signal when the bot is activated
@bot.event
async def on_ready():
    print(f'{bot.user}が正常に実行されました')

# /ask command processing
@bot.command()
async def ask(ctx, *, question):
    async with ctx.typing():
        S_text = S_conversation.predict(input=question)
        await ctx.send(S_text)
       
      # Save memory log to file (If it does not exist, it will be created automatically)
        with open('memory.txt', 'w') as Sf:
            Sf.write(str(S_conversation.memory.load_memory_variables({})))

bot.run(os.environ['TOKEN'])
