import yaml
import pandas as pd
import socket
import sys

sheetname = sys.argv[1]
tournamentID = sys.argv[2]
truck = sys.argv[3]
'''

To-DO
We need to create the other system lists(point the script to these)
We need to figure out the download portion of the CamAssign.xlsx file
'''

'''ping.d on DDP1 - Bolt6 and PI devices
DDP2 - PI-switches and SNMP
Core network split between the two
'''

print(sheetname)
print(tournamentID)
print(truck)



"""
Lets build the Bolt6 camera portion of the yaml first
"""

excel = pd.read_excel(r"CamAssign.xlsx", sheet_name=sheetname, usecols='B:K', nrows=19, header=1) 

data_top = excel.columns
data_missing = excel.isna()


i = 0
devices = []
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
            cameraIp = "172.25.23.14"#socket.gethostbyname(cameraName)
            myobj =  {
            'host': cameraIp,
            'timeout': 1.0,
            'tags':
                [
                
                {'tournament':tournamentID},
                {'location':truck},
                {'hole':holeLocation},
                {'bolt6tfg':cameraLocation},
                {'ip':cameraIp},
                {'rack':'case'},
                {'nightly':False},
                {'hardware':'camera'},
                {'type':'physical'},
                {'env':'prod'},
                {'name':cameraName.lower()},
                {'case':'none'}
                
                ]
                
                }
            devices.append(myobj)
        k = k + 1
    i = i + 1



'''
Lets build the PI device portion of the YAML
'''
power_excel = pd.read_excel(r"CamAssign.xlsx", sheet_name=sheetname, usecols='B:K', nrows=18, header=22) 

data_top = power_excel.columns
data_missing = power_excel.isna()

i = 0

while(i < 18):
    k = 0
    for x in power_excel.iloc[i]:
        
        if(not(data_missing.iloc[i][k]) and ("SC" in str(x))):
            
            casetemp = str(x)
            caseName = 'PI-SC0' + casetemp[3:]
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
            
            myobj = {
                'host': cameraIp,
                'timeout': 1.0,
                'tags':
                    [
                    
                    {'ip':cameraIp},
                    {'env':'prod'},
                    {'type':'physical'},
                    {'rack':'case'},
                    {'hardware':'pi'},
                    {'network':True},
                    {'case':picase},
                    {'name':picase},
                    {'os':'none'},
                    {'priority':'none'},
                    {'grn_server':False},
                    {'location':truck},
                    {'tournament':tournamentID},
                    {'bolt6tfg':piLocation},
                    {'hole':hole}
                    
                    ]
                    
                    }       
            devices.append(myobj)
        k = k + 1
    i = i + 1

with open(f'filename.yaml', 'w',) as f :
        yaml.dump(devices,f,sort_keys=False)








 