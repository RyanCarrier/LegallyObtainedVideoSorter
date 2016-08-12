#!/usr/bin/python
from os import walk
import shutil
import os
import re
from time import sleep

pwd = os.getcwd()

def fix(folder):
    if len(folder) == 0:
        return pwd + '/../'
    if folder[0] == '/':
        return folder
    if folder[0] == '.' and folder[1] == '/':
        return pwd + '/' + folder[2:]
    return pwd + '/' + folder


def fixAndCheck(folder):
    folder = fix(folder)
    if not os.path.isdir(folder):
        print "Folder doesn't exist."
        exit(1)
    return folder


def update_progress(progress):
    print '\r[{0}{1}] {2}%'.format('#' * (progress / 2),
                                   ' ' * ((100 - progress) / 2), progress),
    os.sys.stdout.flush()


folder = raw_input("Enter video folder (default; ./): ")
if not folder:
    folder="./"
folder = fixAndCheck(folder)
targetfolder = raw_input("Enter target folder (default: ../): ")
if not targetfolder:
    targetfolder="../"
targetfolder = fixAndCheck(targetfolder)
response = raw_input("Copy, Move or dry run (default Move): ")
action = 2  #dry run
if response:
    if response[0] == 'c' or response[0] == 'C':
        action = 1  #copy
    elif response[0] == 'd' or response[0] == 'D':
        action = 0  #copy

filenames = []
for (dirpath, dirnames, f) in walk(folder):
    filenames = f
    break

regex = re.compile(r'(.*)(\b[s, S]\d{2}[e, E]\d{2})', re.IGNORECASE)
i = 0
for f in filenames:
    update_progress(100 * i / len(filenames))
    i += 1
    #nobody likes regex, or low quality videos
    if ("HDTV" in f or "720p" in f or "720P" in f or "1080p" in f or "1080P" in f) and ".mkv" in f:

        show, seasonep = regex.match(f).groups()
        showstr = show.strip('.').replace('.', ' ')

        season = seasonep[1:3]
        ep = seasonep[-2:]
        if season[0] == '0':
            season = season[1:]
        path = targetfolder + showstr + "/Season " + season
        if not action:
            print "\nWould move ", folder + '/' + f, " to", path
            continue
        if not os.path.exists(path):
            os.makedirs(path)
        if action == 1:
            shutil.copy(folder + '/' + f, path)
        else:
            os.rename(folder + '/' + f, path+'/'+f)
update_progress(100)
