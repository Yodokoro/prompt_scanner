import discord
import os
import requests
import io
import time
from PIL import Image
from keep_alive import keep_alive


def get_parameters_exif(url):
  pilimage = Image.open(io.BytesIO(requests.get(url).content))
  pilimage.load()
  print(type(pilimage))
  rawdic = pilimage.getexif()
  print(type(rawdic))
  if 'parameters' in pilimage.info:
    parameters = pilimage.info['parameters']
  else:
    parameters = 'No parameters data in this image.\n'
  return parameters


intents = discord.Intents.default()
intents.typing = False
intents.emojis = True
intents.guild_messages = True
intents.guild_reactions = True
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_reaction_add(reaction, user):
  if isinstance(reaction.emoji, discord.Emoji):
    if reaction.emoji.name.startswith('give_me_prompt'):
      for file in reaction.message.attachments:
        msg = file.url + '\n'
        if file.content_type == 'image/png':
          parameters = get_parameters_exif(file.url)
          msg += parameters
        else:
          msg += 'This is not png file.'
        await user.send(msg)


keep_alive()
#try:
client.run(os.getenv('TOKEN'))
#except:
#  print('connection failure: start reconnection in 60[s]')
#    time.sleep(60)
#    os.system("kill 1")
