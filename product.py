import yaml
import pandas as pd
import socket

'''
NOTES
Parameters Required:
sheet name
tid
truck

To-DO
We need to create the other system lists(point the script to these)
We need to include the scripts parameters
We need to figure out the download portion of the CamAssign.xlsx file
'''




"""
Lets build the Bolt6 camera portion of the yaml first
"""

excel = pd.read_excel(r".\CamAssign.xlsx", sheet_name="AT&T Pebble Beach", usecols='B:K', nrows=19, header=1) 

data_top = excel.columns
data_missing = excel.isna()
yamltemplate = ''''''
tournamentID = 'r2024005'
truck = 'sl1'

i = 0

while(i < 18):
    k = 0
    for x in excel.iloc[i]:
        
        if(not(data_missing.iloc[i][k])):
            
            print("###################################")
            print("Hole: " + str(i + 1))
            print("Camera: " + str(x))
            print("Location: " + str(data_top[k]))
            cam = str(x)
            cameraName = cam[0:4] + 'B' +  cam[4:] 
            holeLocation = str(i+1)
            cameraLocation = str(data_top[k]).lower()
            if cameraLocation == 'tee':
                cameraLocation += '1'
            cameraIp = socket.gethostbyname(cameraName)
            yamltemplate += '''- host: {0}
  timeout: 1.0
  tags:
  - tournament:{1}
  - location:{2}
  - hole:{3}
  - bolt6tfg:{4}
  - ip:{0}
  - rack:case
  - nightly:False
  - hardware:camera
  - type:physical
  - env:prod
  - name:{5}
  - case:none\n'''.format(cameraIp,tournamentID,truck,holeLocation,cameraLocation,(cameraName.lower()))
        k = k + 1
    i = i + 1

power_excel = pd.read_excel(r".\CamAssign.xlsx", sheet_name="AT&T Pebble Beach", usecols='B:K', nrows=18, header=22) 

data_top = power_excel.columns
data_missing = power_excel.isna()

i = 0

while(i < 18):
    k = 0
    for x in power_excel.iloc[i]:
        
        if((not(data_missing.iloc[i][k])) and ("SC" in x)):
            
            print("###################################")
            print("Hole: " + str(i + 1))
            print("Power: " + str(x))
            print("Location: " + str(data_top[k]))
            casetemp = str(x)
            caseName = 'PI-SC0' + casetemp[3:]
            with open (r".\PiIPSysListSL1.txt",'r') as pilist:
                lines = pilist.readlines()
                for line in lines:
                    if line.find(caseName) != -1:
                        caseLine = lines.index(line)
            caseIp = (lines[caseLine])[10:-1]
            picase = caseName.lower()
            hole = str(i+1)
            holeLocation = str(data_top[k]).lower()
            if holeLocation == 'tee':
                holeLocation += '1'
            yamltemplate+='''- host: {0}
            timeout: 1.0
            tags:
            - ip:{0}
            - env:prod
            - type:physical
            - rack:case
            - hardware:pi
            - network:True
            - case:{1}
            - name:{1}
            - os:none
            - priority:none
            - grn_server:False
            - location:{2}
            - tournament:{3}
            - bolt6tfg:{4}
            - hole:{5}\n'''.format(caseIp,picase,truck,tournamentID,holeLocation,hole)
        k = k + 1
    i = i + 1

f = open('conf.yaml','a')
f.write(yamltemplate)
f.close()




