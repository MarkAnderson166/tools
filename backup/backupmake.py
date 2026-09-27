import datetime
import subprocess

if str(datetime.datetime.now().hour) in ["15", "17", "20", "23"]:
    subprocess.run(["tar", "-cf", "/media/Media1/BackupDaily/Serenity.tar", "-C", "/home/Mark/SSD2/minecraftserver", "Serenity"], check=True)
