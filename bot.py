import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from functions import get_intent, get_sunset, get_temp, select_learner

load_dotenv(override=True)

luis_key = os.getenv("LUIS_API_KEY")

luis_url = os.getenv("LUIS_REQUEST")

weather_key = os.getenv("WEATHER_API_KEY")

learners = ["Thienvu","Marouan","Armand","Gabriel","Merouane","Aissa","David","Cinthya","Cyrille","Rayanne","William","Thomas","Kamel","Nolan","Pierre-Loic"]
key = os.getenv("DISCORD_KEY")
client = discord.Client()

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    if client.user.mentioned_in(message):   
        
        luis_response = get_intent(luis_key, luis_url, message.content)
        
        intent = luis_response["intent"]
        entity = luis_response["entity"]
            
        if luis_response["score"] > 0.5:
            if intent == "connaitre la température":
                temp = get_temp(weather_key, entity)["temp"]
                await message.channel.send(f"Température Celsius à {entity} : {temp}")
            elif intent == "connaitre coucher soleil":
                sunset = get_sunset(weather_key, entity)['sunset']
                await message.channel.send(f"Coucher de soleil à {entity} : {sunset}")
            elif intent == "trouver un apprenant pour présenter son travail":
                await message.channel.send(f"{select_learner(learners)} doit présenter son travail !")
        elif 'Hello' or 'Hi' or 'Bonjour' in message.content:
            await message.channel.send(f"Hello!")
        else:
            await message.channel.send(f"Vous avez dit '{ message.content }'. je n'ai pas bien compris...")

client.run(key)
