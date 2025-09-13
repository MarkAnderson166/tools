import os
import time
import socket

origin_folder_interface = 'E:\\"World of Warcraft"\\_classic_era_\\Interface'
origin_folder_wtf = 'E:\\"World of Warcraft"\\_classic_era_\\WTF'

origin_temp_interface = 'D:\\share\\Interface'
origin_temp_wtf = 'D:\\share\\WTF'

destination_temp_interface = 'Z:\\Interface'
destination_temp_wtf = 'Z:\\WTF'

destination_folder_interface = 'C:\\"World of Warcraft"\\_classic_era_\\Interface'
destination_folder_wtf = 'C:\\"World of Warcraft"\\_classic_era_\\WTF'

try:

  if 'desktop' in socket.gethostname().lower():

    os.system('echo y|rmdir /s %s'%origin_temp_interface)
    os.system('echo y|rmdir /s %s'%origin_temp_wtf)

    print('delete done, about to copy')
    time.sleep(2)

    os.system('echo d|xcopy %s %s /s /e /h'%( origin_folder_interface, origin_temp_interface))
    os.system('echo d|xcopy %s %s /s /e /h'%( origin_folder_wtf, origin_temp_wtf))

  elif 'laptop' in socket.gethostname().lower():

    os.system('echo y|rmdir /s %s'%destination_folder_interface)
    os.system('echo y|rmdir /s %s'%destination_folder_wtf)

    print('delete done, about to copy')
    time.sleep(2)

    os.system('echo d|xcopy %s %s /s /e /h'%( destination_temp_interface, destination_folder_interface))
    os.system('echo d|xcopy %s %s /s /e /h'%( destination_temp_wtf, destination_folder_wtf))

  else:

    raise Exception("not sure what host i'm running on! ... you told me you're name was: %s"%socket.gethostname())

except Exception as why:

  print("Didn't work! because: %s"% why)

for i in range(5,0,-1):

  print('Closing in %s'%i)

  time.sleep(1)