import yaml
import pandas as pd
import socket

"""
Lets build the Bolt6 camera portion of the yaml first
"""

excel = pd.read_excel(r".\CamAssign.xlsx", sheet_name="American Express", usecols='B:K', nrows=19, header=1) 

data_top = excel.columns
data_missing = excel.isna()
yamltemplate = ''''''
tournamentID = 'r2024005'
truck = 'sl1'

i = 0


power_excel = pd.read_excel(r".\CamAssign.xlsx", sheet_name="American Express", usecols='B:K', nrows=18, header=22) 

data_top = power_excel.columns
data_missing = power_excel.isna()

i = 0

while(i < 18):
    k = 0
    for x in power_excel.iloc[i]:
        
        if(not(data_missing.iloc[i][k])):
            
            print("###################################")
            print("Hole: " + str(i + 1))
            print("Power: " + str(x))
            print("Location: " + str(data_top[k]))
            casetemp = str(x)
            hole = str(i + 1)
            caseName = 'PI-SC0' + casetemp[0:3]
            with open (r"D:\Users\JustinOdel\Development\PowerShell\InTest\DataDogYaml\PiIPSysListSL1.txt",'r') as pilist:
                lines = pilist.readlines()
                for line in lines:
                    if line.find(caseName) != -1:
                        caseLine = lines.index(line)
            caseIp = (lines[caseLine])[10:-2]
            holeLocation = str(data_top[k])
            if holeLocation == 'tee':
                holeLocaiton += '1'
            yamltemplate+='''- community_string: public
  port: 161
  retries: 1
  timeout: 1
  snmp_version: 2
  ip_address: {0}
  tags:
  - ip:{0}
  - env:prod
  - type:physical
  - rack:case
  - hardware:switch
  - network:True
  - case:{1}
  - name:{1}
  - os:none
  - priority:none
  - grn_server:False
  - location:{2}
  - tournament:{3}
  - bolt6tfg:{4}
  - hole:{5}\n'''.format(caseIp,caseName,truck,tournamentID,holeLocation,hole)
        k = k + 1
    i = i + 1

f = open('conf.yaml','a')
f.write(yamltemplate)
f.close()
