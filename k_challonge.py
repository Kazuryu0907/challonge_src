import challonge

import json
import configparser
import os
import errno
import time

TourIds = {}#global


PlayerIds = {}
IdsPlayer = {}
Matches = []
MatchesIds = []
ALLMatches = []
whichC = 0
config_ini_path = "mem.ini"

config_ini = configparser.ConfigParser()
if not os.path.exists("config.ini"):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "config.ini")
config_ini.read("config.ini",encoding='utf-8')
#OFcE6r2H8hvCw6cQwX4hGVnfGxE5Lj55quHhlJEf
#kazuryu_KR
key = config_ini["INFO"]["api_key"]
name = config_ini["INFO"]["username"]
challonge.set_credentials(name,key)

nowRound = 0

def scorecal(UporLow,score):
    try:
        score = list(map(int,score.split('-')))
    except:
        return(-1)
    if len(score) < 2:
        return(-1)
    fir = max(score[0],score[1])
    sec = min(score[0],score[1])
    if UporLow == 0:#up
        return("{0}-{1}".format(fir,sec))
    elif UporLow == 1:#low
        return("{0}-{1}".format(sec,fir))





def openini():
    config_ini = configparser.ConfigParser()
    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
    config_ini.read(config_ini_path,encoding='utf-8')
    return(config_ini)

def addid(config_ini,tour,channelid,tag):
    config_ini[tag][str(channelid)] = tour
    with open(config_ini_path,'w') as configfile:
        config_ini.write(configfile)


def getGuildid(tourid):
    config = openini()
    configItems = dict(config.items("HERE"))
    for i in configItems:
        if configItems[i] == tourid:
            return(i)
    return(-1)


def getIds(tour):
    participants = challonge.participants.index(tour["id"])
    for pers in participants:
        PlayerIds[pers['id']] = pers['display-name']
        IdsPlayer[pers['display-name']] = pers['id']
    return


def getMatchPlayerIds(matches):
    global MatchesIds,Matches,ALLMatches
    MatchesIds = []
    Matches = []
    ALLMatches = []
    for mats in matches:
        try:
            #print(mats)
            ALLMatches.append([PlayerIds[mats['player1-id']],PlayerIds[mats['player2-id']]])
            if mats['state'] == "open":
                Matches.append([PlayerIds[mats['player1-id']],PlayerIds[mats['player2-id']]])
                MatchesIds.append(mats['id'])
        except:
            continue
    print("getMatchPlayerIds:{0}".format(Matches))
    print("ALLMatches:{0}".format(ALLMatches))




def isTeamInMatch(team):
    count = 0
    global whichC
    try:
        for k in Matches:
            for i in range(2):
                if k[i] == team:
                    whichC = i
                    print("Target:{}".format(k))
                    return(count)
            count += 1
    except:
        return(-1)
    return(-1)

def checkResult(tour,scores_csv,TEAM):
    match = challonge.matches.show(tour['id'],MatchesIds[isTeamInMatch(TEAM)])
    if(match['scores-csv'] == scores_csv and match['winner-id'] == IdsPlayer[TEAM]):
        return(1)
    else:
        return(0)

def putMatchResult(tour,scores_csv,TEAM):
    isInMatch = isTeamInMatch(TEAM)
    if(isInMatch == -1):
        return(-1)
    match = challonge.matches.show(tour['id'],MatchesIds[isInMatch])
    matchid = match['id']
    scores_csv = scorecal(whichC,scores_csv)
    if scores_csv == -1:
        return(8)
    match['scores_csv'] = scores_csv
    winner_id = IdsPlayer[TEAM]
    match['winner_id'] = winner_id
    match['state'] = "complete"
    challonge.matches.update(tour['id'],matchid,**match)
    if(checkResult(tour,scores_csv,TEAM) == 1):
        return(1)
    else:
        return(0)

def CheckChangeM4tch(matches):
    thisR = 1
    global nowRound
    flag = False
    isitlast = 0
    isitlastB = False
    for m in matches:
        R = m["round"]
        S = m["state"]
        #print(str(R)+":"+str(S)+":"+str(thisR))
        """
        if flag == True and R != thisR and isitlast == 1:#これ大丈夫かな
            return(0)
        """
        if flag == True and R == thisR:
            if S == "complete":
                return(0)
        
        if flag == True and R != thisR:
            nowRound = thisR
            #print(nowRound)
            return(1)

        if S == "open" and flag == False:
            isitlastB = True
            thisR = R
            flag = True

        if isitlastB == True:
            isitlast += 1 

def CHeck(matches):
    global nowRound
    lastR = 1
    lastS = "complete"
    C = 0
    buff = 0
    flag = False
    for k in matches:
        R = k["round"]
        S = k["state"]
        print("R:{0} now:{2}  C:{1} state:{3} buff:{4}".format(R,C,nowRound,S,buff))
        if S != lastS:
            C += 1
            if flag:
                print('FLAG')
                if(R == lastR and S != lastS):
                    print("FLAG:0")
                    return(0)
            elif R == lastR:
                return(0)
            else:
                flag = True
                buff = R
        else:
            if(R != lastR):
                #print("FUCK")
                nowRound = buff
                break
        lastR = R
        lastS = S
    if C != 0:
        return(1)
    else:
            #print(23)
        return(0)
"""
def CHeck(matches):
    global nowRound
    lastR = 1
    lastS = "complete"
    C = 0
    Rbuff = 0
    flag = False
    for k in matches:
        R = k["round"]
        S = k["state"]
        print("R:{0} now:{2}  C:{1} state:{3}".format(R,C,nowRound,S))
        if S != lastS:
            C += 1
            if R == lastR:
                #print(1)
                return(0)
            else:
                nowRound = R
                break
        lastR = R
        lastS = S
    if C != 0:
        return(1)
    else:
        #print(23)
        return(0)
"""
def show(tourid):
    matches = challonge.matches.index(tourid)
    for m in matches:
        print(m["state"])

def cuttedM4tchRange(matches,nowRound):
    mat = []
    lastR = 0
    C = 0
    final = 0
    #print("nouRound:{}".format(nowRound))
    finalR = matches[-1]["round"]
    matches.append({'round':finalR+1,'state':"open"})
    for m in matches:
        print("round:{0} now:{3} lastR:{1} C:{2} state:{4}".format(m["round"],lastR,C,nowRound,m["state"]))
        if ((m["round"] == nowRound and lastR == nowRound-1) or (m["round"] == nowRound + 1 and lastR == nowRound)):
            mat.append(C)
        final = C
        C += 1
        lastR = m["round"]
    #if len(mat) == 1:
        #mat.append(final)
    
    return(mat)

"""
def cuttedM4tchRange(matches,nowRound):
    mat = [0,0]
    lastR = 1
    C = 0
    final = 0
    print("nouRound:{}".format(nowRound))
    finalR = matches[-1]["round"]
    nRound = nowRound-2#0~
    for m in matches:
        #print(m)
        if(nRound == 1):
            mat[0] = 0
            if(lastR+1 == m["round"]):
                mat[1] = C
                break
        elif(nRound == finalR):
        else:

        lastR = m["round"]
        C += 1
    
    return(mat)
"""
def cuttedM4tch(ALLMatches,matches,mat,nowRound,tourid):
    print("mat:",mat)
    l,h = mat
    cm = matches[l:h]
    loop = h-l
    print((ALLMatches))
    for k in range(loop):
        uniqueNum = cm[k]["suggested-play-order"]
        teams = ALLMatches[l+k]
        yield([nowRound,teams,uniqueNum,tourid,[l+1,h+1]])

def CutteContact(tourid,i):
    tour = challonge.tournaments.show(tourid)
    matches = challonge.matches.index(tourid)
    getIds(tour)
    getMatchPlayerIds(matches)
    yield from cuttedM4tch(ALLMatches,matches,cuttedM4tchRange(matches,i),i,tourid)


def thisismain(tourid,scores_csv,TEAM):
    print("+connecting...")
    tour = challonge.tournaments.show(tourid)
    #print("++")
    print("+getting ids...")
    getIds(tour)
    #print("++")
    print("+getting matches...")
    matches = challonge.matches.index(tour["id"])
    getMatchPlayerIds(matches)
    #print("++")
    print("+putting result...")
    yield(putMatchResult(tour,scores_csv,TEAM))
    matches = challonge.matches.index(tour["id"])
    #if CheckChangeM4tch(matches) == 0:
    if CHeck(matches) == 0:
        print("CheckChangeM4tch:0")
        yield(0)
    else:                   #==1
        print("CheckChangeM4tch:1")
        getMatchPlayerIds(matches)
        yield(1)
        yield(cuttedM4tch(ALLMatches,matches,cuttedM4tchRange(matches,nowRound),nowRound,tourid))

def resetTour(tourid):
    challonge.tournaments.reset(tourid)




#challonge.set_credentials("kazuryu_KR","OFcE6r2H8hvCw6cQwX4hGVnfGxE5Lj55quHhlJEf")
#challonge.tournaments.reset("l2zvqky5")
#print(thisismain("l2zvqky5","33-4","w"))
"""
tour = challonge.tournaments.show("xgj5xik")
matches = challonge.matches.index(tour["id"])
getIds(tour)
getMatchPlayerIds(tour)
print(MatchesIds)
print(Matches)
print(cuttedM4tchRange(matches,3))
"""
"""

tour = challonge.tournaments.show("op7eso53")



print(tour["name"])

participants = challonge.participants.index(tour["id"])
print(len(participants))
getIds(tour)

TEAM = "E"

matches = challonge.matches.index(tour["id"])
print(matches[1])
print("MATCH:{}".format(CheckChangeM4tch(matches)))



getMatchPlayerIds(tour)
print(MatchesIds)
print(Matches)



#print(putMatchResult(tour,"13-12",TEAM))

"""