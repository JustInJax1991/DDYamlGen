import yaml
import pandas as pd
import re
import sys

"""
Lets build the Bolt6 camera portion of the yaml first
"""
sheetname = sys.argv[1]
tournamentID = sys.argv[2]
truck = sys.argv[3]

def getSwtichIP(piIp):
    splitIp = piIp.split('.')
    thirdoctet = int(splitIp[2]) - 1
    splitIp[2] = str(thirdoctet)
    return '.'.join(splitIp)

power_excel = pd.read_excel(r".\CamAssign.xlsx", sheet_name=sheetname, usecols='B:K', nrows=18, header=22) 

data_top = power_excel.columns
data_missing = power_excel.isna()
devices = ""

i = 0

while(i < 18):
    k = 0
    for x in power_excel.iloc[i]:
        caseNum = re.search("\d?\d\d\d",str(x))
        if(not(data_missing.iloc[i][k]) and (caseNum)):
            
            caseName = 'SC0' + caseNum.group()
            picase = 'PI-' + caseName
            with open(f"PiIPSysList{truck}.txt", 'r') as slist:
                lines = slist.readlines()
                for line in lines:
                    if line.find(picase) != -1:
                        caseLine = lines.index(line)
                sLocation = str(data_top[k]).lower()
                if 'tee' in sLocation:
                        sLocation += '1'
            caseIp = (lines[caseLine])[10:-1]
            switchIp = getSwtichIP(caseIp)
            switchcase = caseName.lower()
            hole = i + 1
            myobj = f"\n- community_string: public\n  port: 161\n  retries: 1\n  timeout: 1\n  snmp_version: 2\n  ip_address: {switchIp}\n  timeout: 1.0\n  tags:\n  - ip:{switchIp}\n  - env:prod\n  - type:physical\n  - rack:case\n  - hardware:switch\n  - network:True\n  - case:{switchcase.lower()}\n  - name:{switchcase.lower()}\n  - os:none\n  - priority:none\n  - grn_server:False\n  - location:{truck.lower()}\n  - tournament:{tournamentID}\n  - bolt6tfg:{sLocation}\n  - hole:{hole}"       
            devices = devices + myobj
        k = k + 1
    i = i + 1

with open(f'slxddp2snmpconf.yaml', 'w',) as f :
    f.write(devices)
