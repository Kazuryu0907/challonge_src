import configparser
import os
import errno

config_ini_path = "config.ini"


def openini():
    config_ini = configparser.ConfigParser()
    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
    config_ini.read(config_ini_path,encoding='utf-8')
    return(config_ini)



def tempNomal():
    temp = """次のRound{0}試合は　{1}　vs　{2}　です。
	
部屋名　RLRR{3}　/　パス RL88
	
	🔷ブルー 　　{4}
	🔶オレンジ　{5}
へ入室お願いします。\n"""
    return(temp)

def tempLive():
    temp = """🗻 配信試合🗻
部屋たては運営が行います。
次のRound{0}試合は　{1}　vs　{2}　です。
	
部屋名　RLRR{3}　/　パス RL88
	
	🔷ブルー 　　{4}
	🔶オレンジ　{5}
へ入室お願いします。\n"""
    return(temp)

def tempLine():#B
    temp = "--------------------------------------------\n"
    return(temp)

def tempTemp():
    temp = """
部屋たて設定
🔷challongeの対戦カードの上側のチームが部屋たてをお願いします。
	
アリーナ　チャンピオンズフィールド
エリア　アジア東部
ミューテータ

部屋名　RLRR○○　/　パス　RL88	
--------------------------------------------\n"""
    return(temp)

def tempRound():
    temp = """
-------------------【 Round {0} 】-------------------\n
"""
    return(temp)

def originalNomal():
    config = openini()
    return(config["ANNO"]["nomal"])

def originalLive():
    config = openini()
    return(config["ANNO"]["live"])

def originalLine():
    config = openini()
    return(config["ANNO"]["border"])

def originalTemp():
    config = openini()
    return(config["ANNO"]["temp"])

def originalRound():
    config = openini()
    return(config["ANNO"]["round"])
