# Work with Python 3.6
import discord
import json
import requests

names = []
TOKEN = ""
configFile = open("config.txt","r")
linelist = configFile.readlines()
for line in linelist:
    split = line.split("=")
    if split[0] == "TOKEN":
        TOKEN = split[1]
client = discord.Client()

@client.event
async def on_message(message):
    global names
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!assemblyHelp'):
        msg = "current commands are: \n" \
              " \t !addAssemble @username, \n" \
              " \t !removeAssemble @username, \n" \
              " \t !showAssemble, \n" \
              " \t !clearAssemble, \n" \
              " \t !ASSEMBLE"
        await client.send_message(message.channel, msg)

    if message.content.startswith('!addAssemble'):
        split = message.content.split(" ")
        names.append(split[1])
        msg = "✅ ADDED.".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!removeAssemble'):
        split = message.content.split(" ")
        names.remove(split[1])
        msg = "✅ REMOVED.".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!clearAssemble'):
        split = message.content.split(" ")
        names = []
        msg = "✅ REMOVED EVERYONE.".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!showAssemble'):
        nameString = ""
        for name in names:
            nameString = nameString + name
        if len(names) != 0:
            msg = "This is the squad: "+nameString.format(message)
        else:
            msg = "There isn't a squad.".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!ASSEMBLE'):
        nameList = ""
        for player in names:
            nameList = nameList + player + " "
        if len(names) != 0:
            msg = nameList+" YOU HAVE BEEN SUMMONED FOR A GAME".format(message)
        else:
            msg = "There isn't a squad.".format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run(TOKEN)