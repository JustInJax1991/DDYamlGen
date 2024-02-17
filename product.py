import yaml
import pandas as pd
import socket
import sys
import re


"""
Lets build the Bolt6 camera portion of the yaml first
"""

excel = pd.read_excel(r".\CamAssign.xlsx", sheet_name="AT&T Pebble Beach", usecols='B:K', nrows=19, header=1) 

data_top = excel.columns
data_missing = excel.isna()

i = 0
devices= ""
while(i < 18):
    k = 0
    for x in excel.iloc[i]:
        
        if(not(data_missing.iloc[i][k])):
            
            cam = str(x)
            cameraName = cam[0:4] + 'B' +  cam[4:] 
            holeLocation = i + 1
            cameraLocation = str(data_top[k]).lower()
            if cameraLocation == 'tee':
                cameraLocation += '1'
            cameraIp = socket.gethostbyname(cameraName)
            toWrite = "\n- host: {0}\n  timeout: 1.0\n  tags:\n  - tournament:{1}\n  - location:{2}\n  - hole:{3}\n  - bolt6tfg:{4}\n  - ip:{0}\n  - rack:case\n  - nightly:False\n  - hardware:camera\n  - type:physical\n  - env:prod\n  - name:{5}\n  - case:none".format(cameraIp, tournamentID.lower(), truck.lower(), holeLocation, cameraLocation, cameraName.lower())
            devices = devices + toWrite
        k = k + 1
    i = i + 1

'''
Lets build the PI device portion of the YAML
'''
power_excel = pd.read_excel(r".\CamAssign.xlsx", sheet_name="AT&T Pebble Beach", usecols='B:K', nrows=18, header=22) 

data_top = power_excel.columns
data_missing = power_excel.isna()

i = 0

while(i < 18):
    k = 0
    for x in power_excel.iloc[i]:
        caseNum = re.search("\d?\d\d\d",str(x))
        
        if(not(data_missing.iloc[i][k]) and (caseNum)):
            caseName = 'PI-SC0' + str(caseNum.group())
            with open(f"PiIPSysList{truck}.txt", 'r') as pilist:
                lines = pilist.readlines()
                for line in lines:
                    if line.find(caseName) != -1:
                        caseLine = lines.index(line)
                piLocation = str(data_top[k]).lower()
                if 'tee' in piLocation:
                        piLocation += '1'
            caseIp = (lines[caseLine])[10:-1]
            picase = caseName.lower()
            hole = i + 1
            toWrite = "- host: {0}\n  timeout: 1.0\n  tags:\n  - ip:{0}\n  - env:prod\n  - type:physical\n  - rack:case\n  - hardware:pi\n  - network:True\n  - case:{1}\n  - name:{1}\n  - os:none\n  - priority:none\n  - grn_server:False\n  - location:{2}\n  - tournament:{3}\n  - bolt6tfg:{4}\n  - hole:{5}".format(caseIp, picase, truck.lower(), tournamentID.lower(), piLocation, hole)      
            devices = devices + toWrite
        k = k + 1
    i = i + 1

with open(f'slxddp1pingconf.yaml', 'w',) as f :
        f.write(devices)

f.close()




