#!/usr/bin/python
from os import walk
import shutil
import os
import re

qualitieslower=["pdtv","hdtv","720p","1080p"]
filetypelower=[".mkv",".mp4",".avi",".mpg"]

pwd = os.getcwd()

def fix(folder):
    if folder[0] == '/':
        return folder
    return pwd + '/' + folder


def fixAndCheck(folder):
    folder = fix(folder)
    if not os.path.isdir(folder):
        print "Folder doesn't exist."
        exit(1)
    return folder


def update_progress(progress):
    print '\r[{0}{1}] {2}%'.format('#' * (progress / 2),
                                         ' ' * ((100 - progress) /
                                                2), progress),
    os.sys.stdout.flush()

def move(sourceFolder,sourceFile,destFolder,filenames,action):
    if not action:
        print "\nWould move ", sourceFolder + '/' + sourceFile, " to", destFolder
        return
    if not os.path.exists(destFolder):
        os.makedirs(destFolder)
    update_progress(100 * i / len(filenames))
    if action == 1:
        shutil.copy(sourceFolder + '/' + f, destFolder)
    else:
        os.rename(sourceFolder + '/' + f, destFolder + '/' + f)

default = "./"
folder = raw_input("Enter source folder: %s" % default + chr(8) * len(default))
if not folder:
    folder = default
folder = fixAndCheck(folder)

default = "../"
targetfolder = raw_input("Enter source folder: %s" % default + chr(8) * len(
    default))
if not targetfolder:
    targetfolder=default
targetfolder = fixAndCheck(targetfolder)
response = raw_input("Copy, Move or dry run: M"+chr(8))
action = 2  # Move

if response:
    if response[0].lower() == 'c':
        action = 1  # copy
    elif response[0].lower() == 'd':
        action = 0  # dry run

filenames = []
for (dirpath, dirnames, f) in walk(folder):
    filenames = f
    break

regex = re.compile(r'(.*)(\b[s, S]\d{2}[e, E]\d{2})', re.IGNORECASE)
i = 0
for f in filenames:
    #This is dumb but it fails on files with spaces, but i don't wanna redo the regex tbh
    i += 1
    #if ("WEB" in f.upper() or "PDTV" in f.upper() or "HDTV" in f.upper() or "720P" in f.upper() or "1080P" in f.upper()) and (".mkv" in f.lower() or ".mp4" in f.lower() or ".avi" in f.lower()):
    #if any(x in f.lower() for x in qualitieslower) and any(x in f.lower() for x in filetypelower):
    if any(x in f.lower() for x in filetypelower):
        if regex.match(f) is None:
            if 'ufc' in f.lower():
                move(folder,f,targetfolder+"UFC/"+f.split('.')[1],filenames,action)
            continue
        show, seasonep = regex.match(f.replace(' ','.')).groups()
        showstr = show.strip('.').replace('.', ' ').capitalize()
        showstrsplit=showstr.split(' ')
        showstr=showstrsplit[0]
        x=1
        while x<len(showstrsplit):
            showstr+=' '
            if showstrsplit[x].lower() in ['the','and','to','of']:
                showstr+=showstrsplit[x].lower()
            else:
                showstr+=showstrsplit[x].lower().capitalize()
            x+=1
        season = seasonep[1:3]
        ep = seasonep[-2:]
        if season[0] == '0':
            season = season[1:]
        path = targetfolder + showstr + "/Season " + season
        move(folder,f,path,filenames,action)


update_progress(100)
