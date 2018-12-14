# Work with Python 3.6
import discord
import json
import requests
import fileinput

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

def getTokenFromFile(fileName):
    """GET THE TOKEN FROM THE CONFIG FILE"""
    configFile = open(fileName, "r")
    linelist = configFile.readlines()
    for line in linelist:
        split = line.split("=")
        if split[0] == "TOKEN":
            token = split[1]
            return token

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

"""VARIABLES"""
teamNames = ["ALPHA","BETA","CHARLY","DELTA","ECHO","FOXTROT","GOLF","HOTEL","INDIA",
             "JULIET","KILO","LIMA","MIKE","NOVEMBER","OSCAR","PAPA","QUEBEC","ROMEO",
             "SIERRA","TANGO","UNIFORM","VICTOR","WHISKEY","X-RAY","YANKEE","ZULU"]
squadList = "squadList.txt"

"""GET THE TOKEN FROM A FILE"""
TOKEN = getTokenFromFile("config.txt")

"""SET THE CLIENT"""
client = discord.Client()

@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #HELP
    elif message.content.startswith('!help'):
        embed = discord.Embed(title="Battlefield V Assembler Bot Helper!", description="The following functions are implemented in this bot... every argument is seperated with a whitespace.", color=0x00ff00)
        embed.add_field(name="!addSquad", value="How to use: !addSquad [SQUADNAME] [@USER#XXXX] [@USER#XXXX] ... \n Details: Creates a squad with the given name and the given players", inline=False)
        embed.add_field(name="!removeSquad", value="How to use: !removeSquad [SQUADNAME]                         \n Details: Removes a given squad and all of it's members.", inline=False)
        embed.add_field(name="!showSquads", value="How to use: !showSquads                                       \n Details: Returns an overview of the created squads and their members.", inline=False)
        embed.add_field(name="!squadNames", value="How to use: !squadNames                                       \n Details: Returns an overview of all the squad names.", inline=False)
        embed.add_field(name="!usableSquadNames", value="How to use: !usableSquadNames                           \n Details: Returns an overview of all the squad names that a user can use to make a new squad.", inline=False)
        embed.add_field(name="!ASSEMBLE", value="How to use: !ASSEMBLE [SQUADNAME]                               \n Details: Calls out the squad to play a game!", inline=False)
        embed.add_field(name="Questions?", value="Join the support discord for questions or idea's! https://discord.gg/nT9UM3", inline=False)
        await client.send_message(message.channel, embed=embed)

    #SAVE THE SQUAD TO A FILE
    elif message.content.startswith('!addSquad'):
        playersGiven = message.content.split(" ")
        squadName = playersGiven[1]
        playerList = playersGiven[2:]
        takenTeamNames = getSquadsFromFile(squadList)
        #Name has to be legit & has to be unique
        if squadName in teamNames and squadName not in takenTeamNames:
            stringOfMembers = ""
            for member in playerList:
                if checkUsernameBeforeAdding(member):
                    stringOfMembers = stringOfMembers + " " + member
            try:
                await client.send_message(message.channel, embed=writeSquadToFile(squadList,squadName,stringOfMembers))
            except discord.errors.HTTPException:
                msg = 'There seems to be an error in the command... Check the support page for more info. {0.author.mention}'.format(message)
                removeSquad(squadList, squadName)
                await client.send_message(message.channel,msg)
        else:
            msg = "The squad name is either taken or not on the list of squads.".format(message)
            await client.send_message(message.channel, msg)

    #REMOVE A SQUAD FROM THE FILE
    elif message.content.startswith('!removeSquad'):
        content = message.content.split(" ")
        squadName = content[1]

        #Name has to be legit & has to be used.
        takenTeamNames = getSquadsFromFile(squadList)
        if squadName in teamNames and squadName in takenTeamNames:
            await client.send_message(message.channel, embed=removeSquad(squadList,squadName))
        else:
            msg = "There is no such Squad found.".format(message)
            await client.send_message(message.channel, msg)

    #SHOW AN OVERVIEW OF ALL THE SQUADS
    elif message.content.startswith('!showSquads'):
        msg = ""
        tempMemberList = ""
        for squad in getSquadsFromFile(squadList):
            for member in getSquadMembers(squadList,squad):
                tempMemberList = tempMemberList + " " + member
            msg = msg + (squad + tempMemberList + "\n")
            tempMemberList = ""
        embed = discord.Embed(title="Squad list", description="An overview of what squads are callable.", color=0x00ff00)
        temp = msg.split("\n")
        print(temp)
        for item in temp:
            content = item.split(" ")
            if content[0] != "":
                tempPlayerList = ""
                for player in content[1:]:
                    tempPlayerList = tempPlayerList + " " + player
                embed.add_field(name="Squad: " + content[0], value="Members: " + tempPlayerList, inline=False)
        await client.send_message(message.channel, embed=embed)

    #CALLOUT THE SQUAD
    elif message.content.startswith('!ASSEMBLE'):
        messageContent = message.content.split(" ")
        squadName = messageContent[1]
        takenTeamNames = getSquadsFromFile(squadList)
        # Name has to be legit & has to be unique
        if squadName in teamNames and squadName in takenTeamNames:
            #Call the members of the squad
            msg = callSquad(squadList,squadName)
        else:
            msg = "There is no such Squad found.".format(message)
        await client.send_message(message.channel, msg)

    #Returns the possible squad names
    elif message.content.startswith("!squadNames"):
        nameString = ""
        for name in teamNames:
            nameString = nameString + " " + name + "\n"
        embed = discord.Embed(title="Squad names", color=0x00ff00)
        embed.add_field(name="Possible squad names", value=nameString, inline=False)
        await client.send_message(message.channel,embed=embed)

    #Returns the usable squad names
    elif message.content.startswith("!usableSquadNames"):
        usedNames = getSquadsFromFile(squadList)
        nameString = ""
        for name in teamNames:
            if name not in usedNames:
                nameString = nameString + " " + name + "\n"
        embed = discord.Embed(title="Squad names", color=0x00ff00)
        embed.add_field(name="usable squad names are: ", value=nameString, inline=False)
        await client.send_message(message.channel,embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)