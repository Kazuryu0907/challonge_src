import k_discord as dis
import k_challonge as ch
import displayAnna as an
import time
import threading
import json
import discord
import time
import threading
import asyncio
import sys


ChangeIds = {}
LinkIds = {}

MATCHFORMAT = "ALL"

isitReady = False
AnnoMode = ""

def countDown(cooltime):
    for remaining in range(cooltime, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rComplete!            \n")
def makeAnno(arr,message):
    longann = ""
    liveann = ""
    roles = dis.getGuildFromMessage(message).roles
    c = 0
    Round = -1
    nowRound = 0
    longann = ""
    sliveann = ""


    liveann = ""
    tempann = ""
    nomalann = ""
    lineann = ""
    roundann = ""

    config = dis.openini()
    ann = dict(config.items("ANNO"))
    flag = testAnno_(ann)
    if flag == 0:#加工なし
        nomalann = an.tempNomal()
        liveann = an.tempLive()
        lineann = an.tempLine()
        tempann = an.tempTemp()
        roundann = an.tempRound()
    else:
        if flag>>0 & 1:#下
            nomalann = an.originalNomal()
        if flag>>1 & 1:
            liveann = an.originalLive()
        if flag>>2 & 1:
            lineann = an.originalLine()
        if flag>>3 & 1:#上
            tempann = an.originalTemp()
        if flag>>4 & 1:
            roundann = an.originalRound()
    for i in arr:
        print(i)
        nowRound = i[0]
        if c == 0:
            rang = i[4]
            config = ch.openini()
            for k in json.loads(config["ROUND"][str(message.guild.id)]):
                if rang[0] <= int(k) and rang[1] > int(k):
                    Round = int(k)
            c = 1
        if i[2] != Round: 
            longann += nomalann.format(i[0],i[1][0],i[1][1],i[2],dis.mentionTx(dis.getRoleId(roles,i[1][0])),dis.mentionTx(dis.getRoleId(roles,i[1][1])))
            longann += lineann
        else:
            sliveann += liveann.format(i[0],i[1][0],i[1][1],i[2],dis.mentionTx(dis.getRoleId(roles,i[1][0])),dis.mentionTx(dis.getRoleId(roles,i[1][1])))
            sliveann += lineann
    
    sliveann = roundann.format(nowRound) + sliveann + longann + tempann
    return(sliveann)

def testAnno_(an):
    flag = 0b00000
    C = 0
    for k in an:
        if an[k] != "None":
            flag = flag | 1 << C
        C += 1
    return(flag)
def testAnno():
    arr = [[1,["A","B"],1,"@A","@B"],[1,["C","D"],2,"@C","@D"]]
    C = 0
    longann = ""
    sliveann = ""


    liveann = ""
    tempann = ""
    nomalann = ""
    lineann = ""
    roundann = ""

    config = dis.openini()
    ann = dict(config.items("ANNO"))
    flag = testAnno_(ann)
    print(flag)
    if flag == 0:#加工なし
        nomalann = an.tempNomal()
        liveann = an.tempLive()
        lineann = an.tempLine()
        tempann = an.tempTemp()
        roundann = an.tempRound()
    else:
        if flag>>0 & 1:#下
            nomalann = an.originalNomal()
        if flag>>1 & 1:
            liveann = an.originalLive()
        if flag>>2 & 1:
            lineann = an.originalLine()
        if flag>>3 & 1:#上
            tempann = an.originalTemp()
        if flag>>4 & 1:
            roundann = an.originalRound()


    for i in arr:
        print(i)
        if C == 1: 
            longann += nomalann.format(i[0],i[1][0],i[1][1],i[2],i[3],i[4])
            longann += lineann
            
        else:
            sliveann += liveann.format(i[0],i[1][0],i[1][1],i[2],i[3],i[4])
            sliveann += lineann
            C = 1
    
    sliveann = roundann.format(1) + sliveann + longann + tempann
    return(sliveann)
"""
async def coolan(message,cooltime,arr):
    await asyncio.sleep(cooltime)
    await message.channel.send(makeAnno(arr,message))
"""
@dis.client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(dis.client))


@dis.client.event
async def on_message(message):
    """
    if message.content.startswith('/neko'):
        try:
            message.channel.recipient.dm_channel#ここがDMなら
            config = ch.openini()
            if message.channel.recipient.id in json.loads(config["MASTER"][0]):
                num = message.content.split(" ")

        except:
            pass
    """

    if message.author == dis.client.user:
        if message.content.startswith('[+]'):
            ChangeIds[message.id] = message.content.replace("[+] 上書きしますか？現在のurl:","")
            await message.add_reaction('\N{HEAVY LARGE CIRCLE}')
            await message.add_reaction('\N{CROSS MARK}')
    else:
        global isitReady,AnnoMode
        if isitReady:
            config = dis.openini()#config
            if AnnoMode == "N":
                config["ANNO"]["nomal"] = message.content
            if AnnoMode == "L":
                config["ANNO"]["live"] = message.content
            if AnnoMode == "B":
                config["ANNO"]["border"] = message.content
            if AnnoMode == "T":
                config["ANNO"]["temp"] = message.content
            if AnnoMode == "R":
                config["ANNO"]["round"] = message.content

            with open(dis.config_ini_path,'w',encoding="utf-8") as configfile:
                config.write(configfile)
            isitReady = False
            await message.channel.send("Success!")
            

    """
    if message.content.startswith('/givemeadmin'):
        config = ch.openini()
        try:
            mems = config['MASTER'][0]
            memsD = json.loads(mems)
            memsD.append(message.channel.recipient.id)
            mems = json.dumps(memsD)
            ch.addid(ch.openini(),mems,0,"MASTER")
        except:
            ch.addid(ch.openini(),"["+str(message.channel.recipient.id)+"]",0,"MASTER")#json
        await message.channel.send("give you.")
        #print(message.channel.recipient.id)
    """
    """
    if message.content.startswith('/s'):
        config = ch.openini()
        ch.show(config['HERE'][str(message.guild.id)])
    """
    if message.content.startswith('/r'):#THINKING FACE
        config = ch.openini()
        await message.add_reaction('\N{OPTICAL DISC}')
        ms = message.content
        ms = ms.split(' ')
        isnick = "0"
        try:
            isnick = config["NICK"][str(message.guild.id)]
        except:
            pass
        print(isnick)
        recognitionname = ""
        if(isnick == "0"):
            roles = dis.GetRolesFromMessage(message)
            
            for k in roles:
                if k.name[0] == "[" and k.name[-1] == "]":
                    recognitionname = k.name.replace("[","").replace("]","")
                    break
        elif(isnick == "1"):
            recognitionname = dis.getDisplayNameFromMessage(message)
        result_temp = ch.thisismain(config['HERE'][str(message.guild.id)],ms[1],recognitionname)
        result = result_temp.__next__()
        await message.remove_reaction('\N{OPTICAL DISC}',dis.client.user)
        if result == -1:
            await message.add_reaction('\N{CROSS MARK}')
            await message.channel.send("試合中の{0}のMatchが見つかりません".format(recognitionname))
        elif result == 0:
            await message.add_reaction('\N{CROSS MARK}')
            await message.channel.send("送信Error")
        elif result == 1:               #成功時
            await message.add_reaction('\N{HEAVY CHECK MARK}')
            #await message.channel.send("送信完了 point:{0}".format(ms[1]))
            if result_temp.__next__() == 1:#アナウンス判定
                config = ch.openini()
                try:
                    cooltime = int(float(config['COOL'][str(message.guild.id)])*60)
                except:
                    cooltime = 0
                countDown(cooltime)
                await message.channel.send(makeAnno(result_temp.__next__(),message))
        elif result == 8:
            await message.add_reaction('\N{CROSS MARK}')
            await message.channel.send("無効なフォーマットです")
    
    if message.content.startswith("/settype"):
        ms = message.content
        ms = ms.split(' ')
        tourid = ms[1]
        config = ch.openini()
        ch.addid(config,tourid,message.guild.id,"TYPE")
        config = ch.openini()
        await message.channel.send("設定しました:{0}".format(config["TYPE"][str(message.guild.id)]))

    if message.content.startswith("/わんわんお"):
        config = ch.openini()
        ch.resetTour(config['HERE'][str(message.guild.id)])
    
    """
    if message.content.startswith("/show"):
        ms = message.content
        ms = ms.split(' ')
        if ms[1] == "id":
            config = ch.openini()
            try:
                urlid = config['HERE'][str(message.guild.id)]
                await message.channel.send(urlid)
            except:    
                await message.channel.send("登録なし")
    """
    """
    if message.content.startswith("/Hi"):
        try:
            config = ch.openini()
            arr = json.loads(config['MASTER'][str(0)])
            await dis.DM("unchi",arr,message)
        except:
            import traceback
            traceback.print_exc()
    """
    if message.content.startswith("/usenickname"):
        config = ch.openini()
        ch.addid(config,"1",message.guild.id,"NICK")
        await message.channel.send("設定しました usenickname:1")
        
    if message.content.startswith("/userolename"):
        config = ch.openini()
        ch.addid(config,"0",message.guild.id,"NICK")
        await message.channel.send("設定しました usenickname:0")

    if message.content.startswith("/Tanno"):
        await message.channel.send(testAnno())
        
    if message.content.startswith("/setid"):
        ms = message.content
        ms = ms.split(' ')
        tourid = ms[1]
        config = ch.openini()
        try:
            oldtourid = config['HERE'][str(message.guild.id)]
            LinkIds[oldtourid] = tourid
            await message.channel.send("[+] 上書きしますか？現在のurl:{}".format(oldtourid))
        except:
            ch.addid(config,tourid,message.guild.id,"HERE")
            await message.channel.send("更新しました    TournamentId:{0} GuildId:{1}".format(tourid,message.guild.id))
    if message.content.startswith("/state"):
        config = ch.openini()
        ch.show(config['HERE'][str(message.guild.id)])

    if message.content.startswith("/setlive"):
        c = message.content.split(" ")
        Rs = c[1].split(",")
        ch.addid(ch.openini(),json.dumps(Rs),message.guild.id,"ROUND")
        await message.channel.send("設定しました:{}".format(json.dumps(Rs)))

    if message.content.startswith("/start"):
        await message.add_reaction('\N{OPTICAL DISC}')
        #if dis.checkRoles("運営",dis.GetRolesFromMessage(message)):
        config = ch.openini()
        await message.channel.send(makeAnno(ch.CutteContact(config['HERE'][str(message.guild.id)],1),message))
        await message.add_reaction('\N{HEAVY CHECK MARK}')
        """
        else:
            await message.clear_reaction('\N{OPTICAL DISC}')
            await message.channel.send("権限がありません")
        """

    if message.content.startswith("/setcooltime"):
        c = message.content.split(" ")
        ch.addid(ch.openini(),c[1],message.guild.id,"COOL")
        #config['COOL'][str(message.guild.id)] = c[1]
        config = ch.openini()
        await message.channel.send("設定しました:{}[min]".format(config['COOL'][str(message.guild.id)]))

    if message.content.startswith("/show"):
        config = ch.openini()
        tourid = "None"
        live = "None"
        cooltime = 0
        try:
            tourid = config['HERE'][str(message.guild.id)]
            live = config['ROUND'][str(message.guild.id)]
            cooltime = config['COOL'][str(message.guild.id)]
        except:
            pass
        await message.channel.send("TournamentId : {0}\nLivePlayOder : {1} cooltime : {2}".format(tourid,live,cooltime))
    
    if message.content.startswith("/cons"):
        config = ch.openini()
        ch.show(config['HERE'][str(message.guild.id)])
    
    if message.content.startswith("/anno"):
        m = message.content.split(" ")
        whi = m[1]
        if whi == "N" or whi == "L" or whi == "B" or whi == "T" or whi == "R":
            isitReady = True
            AnnoMode = whi
            await message.channel.send("[++]Ready by Mode : {}".format(whi))
        else:
            await message.channel.send("無効なModeです : {}".format(whi))

    if message.content.startswith("/n"):
        nickname = dis.getDisplayNameFromMessage(message)
        print(nickname)

#HEHEHE
@dis.client.event
async def on_reaction_add(reaction,user):
    if reaction.message.content.startswith("[+]") and user != dis.client.user:
        if(reaction.emoji == "\N{HEAVY LARGE CIRCLE}"):
            ch.addid(ch.openini(),LinkIds[ChangeIds[reaction.message.id]],reaction.message.guild.id,"HERE")
            await reaction.message.delete()
            await reaction.message.channel.send("更新しました    TournamentId:{0} GuildId:{1}".format(LinkIds[ChangeIds[reaction.message.id]],reaction.message.guild.id))
            del LinkIds[ChangeIds[reaction.message.id]]
            del ChangeIds[reaction.message.id]
            
            
        elif (reaction.emoji == "\N{CROSS MARK}"):
            del LinkIds[ChangeIds[reaction.message.id]]
            del ChangeIds[reaction.message.id]
            await reaction.message.delete()
            await reaction.message.channel.send("取り消しました")
    #print(user.roles)


try:
    dis.client.run(dis.TOKEN())
except discord.errors.LoginFailure:
    print("Token Error.")
    input("press any key...")