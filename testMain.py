# Work with Python 3.6
import praw
import discord
import json
import requests
import fileinput
import os
import ctypes
import queue
from idna import idnadata
import configparser
import glob

def readMemeList(memeList):
    file = open(memeList, "r")
    lines = file.readlines()
    file.close()
    filenames = []
    for line in lines:
        filenames.append(line)
    return filenames

def writeToMemeList(memelist,line):
    file = open(memelist, "r")
    lines = file.readlines()
    file.close()

    file = open(memelist,"w")
    for line in lines:
        file.write(line + "\n")
    file.write(line + "\n")
    file.close()

def loadMemesToList():
    return os.listdir(path=FILEPATH)

def get_pictures_from_subreddit(data, subreddit):
    global extension
    for i, x in enumerate(data):
        current_post = data[i]['data']
        image_url = current_post['url']
        if '.png' in image_url:
            extension = '.png'
        elif '.jpg' in image_url or '.jpeg' in image_url:
            extension = '.jpeg'
        elif 'imgur' in image_url:
            image_url += '.jpeg'
            extension = '.jpeg'
        else:
             continue
        # redirects = False prevents thumbnails denoting removed images from getting in
        image = requests.get(image_url, allow_redirects=False)
        if (image.status_code == 200):
            try:
                print("WRITING FILE: "+str(i))
                output_filehandle = open(FILEPATH + str(i) + extension, 'wb')
                output_filehandle.write(image.content)
                path = str(FILEPATH)+str(i)+str(extension)
                print(path)
                writeToMemeList(memeFileList,path)
            except Exception as e:
                print(str(e))
    print("Done getting images!")

def get_image():
    config = configparser.ConfigParser()
    config.read('args.ini')
    top = config['Default']['top']
    subreddit = config['Default']['subreddit']
    number = config['Default']['number']
    url = 'https://www.reddit.com/r/{}/top/.json?sort=top&t={}&limit={}'.format(subreddit, top, number)
    response = requests.get(url, headers={'User-agent': USERAGENT})
    data = response.json()['data']['children']
    return get_pictures_from_subreddit(data, subreddit)

def getSquadsFromFile(filename):
    file = open(filename, "r")
    takenTeamNames = []
    # Adds all of the taken team names so there won't be dupes
    for line in file:
        tag = line.split(" ")
        takenTeamNames.append(tag[0])
    return takenTeamNames

def writeSquadToFile(squadList,squadName,squadMembers):
    file = open(squadList, "r")
    lines = file.readlines()
    file.close()

    file = open(squadList,"w")
    for line in lines:
        file.write(line + "\n")
    file.write(squadName + " " + squadMembers)
    file.close()
    embed = discord.Embed(title="Squad Added!",
                          description=squadName,
                          color=0x00ff00)
    embed.add_field(name="Members: ", value=squadMembers, inline=False)
    return embed

def getFromFile(fileName,command):
    """GET THE TOKEN FROM THE CONFIG FILE"""
    file = open(fileName, "r")
    linelist = file.readlines()
    for line in linelist:
        if line.startswith("#") or line == "":
            continue
        else:
            split = line.split("=")
            if split[0] == command:
                item = split[1]
                return item[:len(item) - 1]
            else:
                continue

def callSquad(filename,squadName):
    file = open(filename,"r")
    for line in file:
        if line.startswith(squadName):
            content = line.split()
            members = ""
            for name in content[1:]:
                members = members + " " + name
            return "YOUR SQUAD IS CALLED UPON! ASSEMBLE NOW! " + members
    return "Squad Not Found!"

def removeSquad(filename,squadName):
    file = open(filename, "r+")
    lines = file.readlines()
    file.close()

    file = open(filename,"w")
    for line in lines:
        if not line.startswith(squadName):
            file.write(line + "\n")
    file.close()

    embed = discord.Embed(title="Squad removed!",
                          description=squadName,
                          color=0x00ff00)
    return embed

def getSquadMembers(filename,squadName):
    file = open(filename, "r")
    for line in file:
        if(line.startswith(squadName)):
            content = line.split()
    memberList = content[1:]
    return memberList

def checkUsernameBeforeAdding(name):
    if name.startswith("<"):
        if name.endswith(">"):
            if name[1] == "@":
                return True
    return False

"""GET THE SECRETS FROM A FILE"""
configFile = "config.txt"
TOKEN = getFromFile(configFile,"TOKEN")
client_id = getFromFile(configFile,"client_id")
username = getFromFile(configFile,"username")
password = getFromFile(configFile,"password")
client_secret = getFromFile(configFile,"client_secret")
USERAGENT = "fake_user_agent v1.0"
FILEPATH = os.path.join(os.getcwd(), r'C:\Users\Twan\PycharmProjects\Discord\images\memes\\')
memeFileList = "memelist.txt"
memeFiles = readMemeList(memeFileList)
print(len(memeFiles))

"""SET THE CLIENT"""
client = discord.Client()

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent='testscript by /u/fakebot3',
                     username=username)

@client.event
async def on_message(message):
    global memeFileList
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    elif message.content.startswith('!test'):
        print("Message ID: " + str(message.id))
        print("Message Type: " + str(message.type))
        print("Message Channel: " + str(message.channel))
        """Check whether it's a DM or a server message."""
        if message.server is not None:
            print("Message on server: " + str(message.server))
            members  = ""
            for member in message.server.members:
                members += str(member) + ", Playing: " + str(member.game) + "\n "
            print("Members on server: " + members)

    elif message.content.startswith("!dankmeme"):
        if(len(memeFiles) < 1):
            print(len(memeFiles))
            await client.send_message(message.channel,"No memes, let's me hook you up with a few, brb.")
            get_image()
            await client.send_message(message.channel,"I got 'm.")
            await client.send_file(message.channel,str(FILEPATH)+memeFileList[0])
        else:
            #Send a file
            await client.send_file(message.channel,str(FILEPATH)+memeFileList[0])
    #delete the [0] object.
    os.remove(FILEPATH+memeFileList[0])
    memeFileList.remove(0)


@client.event
async def on_ready():
    print('Logged in as')
    print("Username: " + client.user.name)
    print("User ID:" + client.user.id)
    print('------')

client.run(TOKEN)