import discord
import os
import requests
import json 
import random

client = discord.Client()

help_flags = ["give up", "giving up", "discouraged", "sad", "lazy", "unmotivated", "depressed", "=-=", "unhappy", "miserable", "depressing"]

starting_motivations = ["You can do it!", "Hang in there!", "Don't give up!", "You are going to be ok!"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

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
  
  if any(word in msg for word in help_flags):
    await message.channel.send(random.choice(starting_motivations))

client.run(os.getenv('TOKEN'))