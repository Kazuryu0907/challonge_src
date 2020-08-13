import discord 
import configparser
import os
import errno

config_ini_path = "config.ini"

client = discord.Client()

def openini():
    config_ini = configparser.ConfigParser()
    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
    config_ini.read(config_ini_path,encoding='utf-8')
    return(config_ini)

def getDisplayNameFromMessage(message):
    user = message.author
    nickname = user.display_name
    return(nickname)

def getGuildFromMessage(message):
    guildid = message.guild.id
    guild = client.get_guild(guildid)
    return(guild)

def getMemberFromMessage(message,guild):
    memberid = message.author.id
    member = guild.get_member(memberid)
    return(member)

def GetRolesFromMessage(message):#送信者の
    guild = getGuildFromMessage(message)
    member = getMemberFromMessage(message,guild)
    return(member.roles)

@client.event
async def DM(M,arr,message):
    for k in arr:
        guild = getGuildFromMessage(message)
        member = guild.get_member(k)
        dm = await member.create_dm()
        await dm.send(M)

def checkRoles(role,roles):
    for k in roles:
        if role == k.name:
            return(1)
    return(0)
    
def getRolesFromGuildid(id):
    guild = client.get_guild(id)
    print(guild)
    return(guild.roles)

def getRoleId(arr,name):
    rename = "["+name+"]"
    for k in arr:
        if k.name == rename:
            return(k.id)
    return(-1)

def TOKEN():
    config = openini()
    try:
        token = config["INFO"]["token"]
        return(token)
    except:
        return("here")
    #NjgxMTQ1MzM5ODkzMjUyMTEy.XlkvIQ.VXlO8p2BCwA0DKsDlllHfKC4I_I
    #return('NjgxMTQ1MzM5ODkzMjUyMTEy.XlkvIQ.VXlO8p2BCwA0DKsDlllHfKC4I_I')

def mentionTx(id):
    return("<@&"+str(id)+">")
"""
#py -3 .\bot.py
"""

