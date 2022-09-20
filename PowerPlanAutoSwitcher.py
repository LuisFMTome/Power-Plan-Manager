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
u = "powercfg /setactive "
b = "powercfg /setactive "
avgCPU = "(Get-WmiObject win32_processor | Measure-Object -property LoadPercentage -Average | Select Average ).Average"
avgCPUList = []
r = os.popen('powercfg /list')
######################################################
for line in r:
    if "Ultimate" in line:
        u += line.split(" ")[3]
        if "*" in line:
            previousPlan = "UM"
    elif "Balanced" in line:
        b += line.split(" ")[3]
        if "*" in line:
            previousPlan = "BM"

r.close()
######################################################
icon = pystray.Icon("Power Plan Switch", 
                    img.open("icon.png"), 
                    "Power Plan Switch")

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
    
    avgCPUList.append(int(subprocessRun(avgCPU, True, True).stdout.lower()))
    
    if len(avgCPUList) == 10:
        
        if previousPlan == "BM" and int(sum(avgCPUList)/len(avgCPUList)) >= 40:
            subprocessRun(u, False, False)
            previousPlan = "UM"

        elif previousPlan == "UM" and int(sum(avgCPUList)/len(avgCPUList)) < 40:
            subprocessRun(b, False, False)
            previousPlan = "BM"

        avgCPUList.pop(0)

    time.sleep(1)
######################################################