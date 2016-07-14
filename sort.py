#/usr/bin/python
from os import walk
import shutil
import os
import re

pwd = os.getcwd()


def fix(folder):
    if len(folder) == 0:
        return pwd + '/../'
    if folder[0] == '/':
        return folder
    return pwd + '/' + folder


def fixAndCheck(folder):
    folder = fix(folder)
    if not os.path.isdir(folder):
        print "Folder doesn't exist."
        exit(1)
    return folder


folder = raw_input("Enter video folder (default; ../):")
targetfolder = raw_input("Enter target folder (default: ../):")

response = raw_input("Copy, Move or dry run")
action = 0  #dry run
if response[0] == 'c' or response[0] == 'C':
    action = 1  #copy
elif response[0] == 'm' or response[0] == 'm':
    action = 2  #copy

filenames = []
for (dirpath, dirnames, f) in walk(folder):
    filenames = f
    break

regex = re.compile(r'(.*)(\b[s, S]\d{2}[e, E]\d{2})', re.IGNORECASE)
for f in filenames:
    #nobody likes regex, or low quality videos
    if "720p" not in f and "720P" not in f and "1080p" not in f and "1080P" not in f:
        show, seasonep = regex.match(f).groups()
        showstr = show.strip('.').replace('.', ' ')

        season = seasonep[1:3]
        ep = seasonep[-2:]
        if season[0] == '0':
            season = season[1:]
        path = targetfolder + showstr + "/Season " + season
        if not action:
            print "Would move ", folder + '/' + f, " to", path
            continue
        if not os.path.exists(path):
            os.mkdirs(path)
        if action == 1:
            shutil.copy2(folder + '/' + f, path)
        else:
            shutil.move(folder + '/' + f, path)
