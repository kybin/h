import os

tempfolder = hou.expandString('$TEMP')

files = ["/".join([tempfolder, file]) for file in os.listdir(tempfolder) if file.split(".")[-1]=='hip']
files.sort(key=lambda x: os.path.getmtime(x))
lasthipfile = files[-1]

hou.hipFile.load(lasthipfile)