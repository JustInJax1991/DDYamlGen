import yaml
import pandas as pd



excel = pd.read_excel(r".\CamAssign.xlsx", sheet_name="American Express", usecols='B:K', nrows=19, header=1) 

data_top = excel.columns
data_missing = excel.isna()

i = 0

while(i < 18):
    k = 0
    for x in excel.iloc[i]:
        
        if(not(data_missing.iloc[i][k])):
            
            print("###################################")
            print("Hole: " + str(i + 1))
            print("Camera: " + str(x))
            print("Location: " + str(data_top[k]))
        k = k + 1
    i = i + 1



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
        k = k + 1
    i = i + 1




ip_excel = pd.read_excel(r".\IPDet.xlsx", sheet_name="ShotLink 1", usecols='A, Y', nrows=144) 
data_missing = ip_excel.isna()

i = 0

while(i < 144):
    k = 0
    while(k < 2):
        if(not(data_missing.iloc[i][k])):
            print(ip_excel.iloc[i][k])
        k = k + 1
    i = i + 1