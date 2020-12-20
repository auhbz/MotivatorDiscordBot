import discord
import os
import requests
import json 
import random
from replit import db

client = discord.Client()

help_flags = ["give up", "giving up", "discouraged", "sad", "lazy", "unmotivated", "depressed", "=-=", "unhappy", "miserable", "depressing"]

starting_motivations = ["You can do it!", "Hang in there!", "Don't give up!", "You are going to be ok!"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def update_motivations(motivating_message):
  if "motivations" in db.keys():
    motivations = db["motivations"]
    motivations.append(motivating_message)
    db["motivations"] = motivations
  else:
    db["motivations"] = [motivating_message]

def delete_motivations(index):
  motivations = db["motivations"]
  if len(motivations) > index:
    del motivations[index]
    db["motivations"] = motivations

@client.event
async def on_ready():
  print('{0.user} is ready!'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if message.content.startswith('$hello'):
    await message.channel.send('Hello there!')
  
  if message.content.startswith('$motivate'):
    quote = get_quote()
    await message.channel.send(quote)
  
  options = starting_motivations
  if "motivations" in db.keys():
    options = options + db["motivations"]

  if any(word in msg for word in help_flags):
    await message.channel.send(random.choice(options))

  if msg.startswith("$add"):
    motivating_message = msg.split("$add ", 1)[1]
    update_motivations(motivating_message)
    await message.channel.send("Motivating message has been added!")

  if msg.startswith("$remove"):
    motivations = []
    if "motivations" in db.keys():
      index = int(msg.split("$remove ", 1)[1])
      delete_motivations(index)
      motivations = db["motivations"]
    await message.channel.send(motivations)

client.run(os.getenv('TOKEN'))