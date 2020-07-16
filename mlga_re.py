import os
import sys
import time
import re
import steamapi
import ast
import html
import huepy 
import webbrowser
import datetime  
import json
from huepy import *
import linecache
import tkinter as tk
import threading
from PIL import ImageTk,Image
import tkinter.font as font

killer_list = {
    "Cannibal": "CA",
    "Clown": "GK",
    "Clown_": "Clown",
    "Demogorgon": "QK",
    "Doctor": "DO",
    "Doctor_": "DOW04",
    "Doctor__": "Killer07",
    "Ghostface": "OK",
    "Hag": "HA",
    "Hag_Witch": "WI",
    "Hag_Witch_": "Witch",
    "Hillbilly": "HB",
    "Hillbilly_CW": "TC",
    "Hillbilly_OG": "Hillbilly",
    "Huntress": "BE",
    "Legion": "KK",
    "Legion_": "Legion",
    "Nightmare": "SD",
    "Nurse": "TN",
    "Nurse_Sally": "NR",
    "Nurse_": "Nurse",
    "Oni": "SwedenKiller",
    "Pig": "FK",
    "Plague": "MK",
    "Plague_": "Plague",
    "Shape": "MM",
    "Spirit": "HK",
    "Spirit_": "Spirit",
    "Trapper": "TR",
    "Trapper_03": "TRW03",
    "Trapper_04": "TRW04",
    "Trapper_Ch": "Chuckles",
    "Trapper_S01": "S01",
    "Trapper_": "Trapper",
    "Wraith_0": "TW",
    "Wraith_1": "WR",
    "Wraith_WR": "Wraith",
    "DeathSlinger": "UkraineKiller",
    "DeathSlinger_2" : "UK", 
    "Executioner": "K20"
}

user = os.getlogin()
log_path = "C:/Users/" + user + \
    "/AppData/Local/DeadByDaylight/Saved/Logs/DeadByDaylight.log"

steam_profile_url_prefix = "https://steamcommunity.com/profiles/"

print(good("Hello " + user + "!"))

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def getSteamName(steamID):
    steam_profile_url_prefix = "https://steamcommunity.com/profiles/"
    steamapi.core.APIConnection(
        api_key="BB78F4C62B0635A4C06157493BFE5758", validate_key=True)
    Playername = steamapi.user.SteamUser(steamID).name
    return Playername


def searchKillerNameInLine(line):
    regex = r"[1-9][0-9]{16}"
    match = re.search(regex, line)
    if match:
        lastSteamId = match.group(0)
        return lastSteamId

def get_key(my_dict, val): 
    for key, value in my_dict.items(): 
        if val == value: 
            return key 
  
    return "NULL"

def scanKillerTypeFromLine(line):
    regex = r"(?<=LogCustomization: -->\s)(\w[^_]*)"
    match = re.search(regex, line)
    killerCode = match.group(0)
    return killerCode  


def dumpToFile(list):
    # open output file for writing
    with open('blacklist.txt', 'w') as filehandle:
        json.dump(list, filehandle)

def loadFromFile():
    with open('blacklist.txt', 'r') as filehandle:  
        basicList = json.load(filehandle)  
        return basicList 

def checkIfAlreadyInBlacklist():
    pass

def testDuplicateKiller(text):
    reg = r"^[^_]+(?=_)"
    match = re.search(reg, text)
    if match:
        matchedText = match.group(0)
        return matchedText 


class Killer:
    number = int()
    steamId64 = int()
    firstseen = str()
    lastseen = str()
    names = str()
    blocked = str()
    notes = str()
    
    Killerdata = {
       1: steamId64, 
       2: lastseen,
       3: names,
       4: blocked, 
       5: notes
    }

def mainLoop():
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            print("Loading Succeeded! Enjoy")
            try:
                searchlines = f.readlines()
                #lastKiller = 0
                lastSteamId = int()
                customFound = int()
                lastCharSeen = str()
                lastSteamIdParsed = int()
                killerSteamName = str()
                for i, line in enumerate(searchlines):
                    if "AddSessionPlayer" in line:
                        regex = r"[1-9][0-9]{16}"
                        match = re.search(regex, line)
                        if match:
                            lastSteamId = match.group(0)

                    if lastSteamId !=0 and (lastSteamId is not None) and any([v in line for v in killer_list.values()]):
                        #print("DEBUG: " + " ENtered main LOOP" )          
                        killerSteam = lastSteamId
                        killerSteamName = getSteamName(killerSteam)
                        lastSteamIdParsed = lastSteamId 
                        lastSteamId = None
                        #webbrowser.open(steam_profile_url_prefix + str(killerSteam))
                        
                    if "LogCustomization: --> " in line:
                        customFound += 1						
                        if customFound > 1:
                            lastSteamId = None
                            customFound = 0
                        
                        value = scanKillerTypeFromLine(line)
                        killerCharName = get_key(killer_list, value)
                        if lastCharSeen == killerCharName:
                            pass
                        elif killerCharName != "NULL" and lastCharSeen != killerCharName:
                            lastCharSeen = killerCharName    
                label1.config(text ="Killer Steam Name, ID:  "+ str(killerSteamName)+ " " + str(lastSteamIdParsed))
                label2.config(text ="Playing Character: "+ str(lastCharSeen), fg="red")
                            
            except:
                PrintException()
                sys.exit()
        f.close()        
        root.after(3500, mainLoop)
    except KeyboardInterrupt:
        f.close()
        sys.exit(1)
        print("Bye " + user + " ! " + "Stay toxic and dont forget to teabag!")

# def my_fun(todo):
    # w=b2.cget('width')
    # if(todo=='increase'):
       # w=w+5
    # else:
       # w=w-5
    # b2.config(width=w)


root = tk.Tk()
root.title('MLGA Reborn v1.0')

label1 = tk.Label(root, text="")
label2 = tk.Label(root, text="")

button = tk.Button(text = "Quit" ,command = root.destroy, font = 'bold')
button.config(borderwidth = 5)
myFont = font.Font(size = 12)
label1['font'] = myFont
label2['font'] = myFont 
button['font'] = myFont 

label1.pack(side = tk.TOP, anchor = tk.N, fill = tk.X)
label2.pack(side = tk.LEFT, anchor = tk.N, fill = tk.X)
button.pack(side = tk.RIGHT, anchor = tk.N, fill = tk.X )

mainLoop()
root.mainloop()
