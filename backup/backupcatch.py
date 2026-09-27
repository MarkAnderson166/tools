from urllib.request import urlopen
import os

os.makedirs(os.path.expanduser("~/Documents/BackupDaily"), exist_ok=True)

with urlopen("http://192.168.0.140:8765/Serenity.tar") as response:
    with open(os.path.expanduser("~/Documents/BackupDaily/Serenity.tar"), "wb") as file:
        file.write(response.read())
