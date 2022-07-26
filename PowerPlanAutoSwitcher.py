######################################################
import os
import time
import pystray
import subprocess
from PIL import Image as img
from pystray import Icon, Menu, MenuItem
from threading import Thread
######################################################
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= (
    subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
)
startupinfo.wShowWindow = subprocess.SW_HIDE
######################################################
previousPlan = ""
platforms = ["steam", "EpicGamesLauncher"]
u = "powercfg /setactive "
b = "powercfg /setactive "
gP = "Get-Process"
cmdMSI = "& 'C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe' "
iconName = "Power Plan Switch"
iconImage = img.open("icon.png")
######################################################
r = os.popen('powercfg /list')

for line in r:
    if "Ultimate" in line:
        u += line.split(" ")[3]
        previousPlan = "UM"
    elif "Balanced" in line:
        b += line.split(" ")[3]
        previousPlan = "BM"

r.close()
######################################################
icon = pystray.Icon(iconName, iconImage, iconName)

def iconStart():
    icon.run()

def subprocessRun(cmd, co, t):
    
    if co and t:
        return subprocess.run(["powershell", "-Command", cmd], 
                        capture_output=co, text=t, 
                        startupinfo=startupinfo)
    else:
        subprocess.run(["powershell", "-Command", cmd], 
                        capture_output=co, text=t, 
                        startupinfo=startupinfo)
######################################################
thread = Thread(target = iconStart)
thread.start()
######################################################
while True:

    platCount = 0
    processList = subprocessRun(gP, True, True)

    for platform in platforms:
        if platform in processList.stdout:
            platCount += 1

    if platCount > 0:
        if previousPlan == "BM":
            subprocessRun(u, False, False)
            subprocessRun(cmdMSI+"-Profile1", False, False)
            previousPlan = "UM"
    else:
        if previousPlan == "UM":
            subprocessRun(b, False, False)
            subprocessRun(cmdMSI+"-Profile2", False, False)
            previousPlan = "BM"
    
    time.sleep(0.5)
######################################################
