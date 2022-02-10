import pandas
import numpy as np
import sys

df1 = pandas.read_csv(".//ExA//ExA//grandi//2018_LiceoGalilei1.rtf", encoding ="utf_8")

total_attempt=0
max_instruction=0
index_instruction=0
for i in range(len(df1)):
    if df1._get_value(i,0, takeable = True)=="STOP PROGRAM;":
        total_attempt = total_attempt+1
        if(max_instruction<index_instruction):
            max_instruction=index_instruction
        index_instruction=0
    else:
        index_instruction=index_instruction+1
        

instruction = np.empty((total_attempt,max_instruction,6), dtype='U256')
index_instruction=0
attempt=0
for i in range(len(df1)):
    if df1._get_value(i,0, takeable = True)=="STOP PROGRAM;":
        attempt= attempt + 1
        index_instruction=0
    else:
        instruction[attempt][index_instruction]=df1.iloc[i].values
        index_instruction=index_instruction+1
     
np.set_printoptions(threshold=sys.maxsize)  
print(instruction)


def difference(row1, row2):
    if(row1[0]!=row2[0]):
        return "Change blockname to"+row2[0]
    else:
        if(row1[1]!=row2[1]):
            return "Change type"+row2[1]
        else:
            if(row1[2]!=row2[2]):
                return "Change param"+ row2[2]
            if(row1[3]!=row2[3]):
                return "Change param"+ row2[3]
            if(row1[4]!=row2[4]):
                return "Change param"+ row2[4]
            if(row1[5]!=row2[5]):
                return "Change param"+ row2[5]
    return ""        
    
print("\n\nTRACE:")
for i in range(total_attempt-1):
    for j in range(len(instruction[i])):
        ret=difference(instruction[i][j],instruction[i+1][j])
        if(ret!=""):
            print(ret)

### colonne
### caseid; timestamp; activity;Blockname, Type, 1st-param, 2nd-param, 3rd-param, 4th-param 
### 2018_galilei_1;1;Set moveSteering on for rotation, MoveSteering, OnForRotations, Rotations = 1, Speed = 100, Steering = 0, MotorPorts = 123; 
### 2018_galilei_1;2;No action, MoveSteering, OnForRotations, Rotations = 1, Speed = 100, Steering = 0, MotorPorts = 123; 
### 2018_galilei_1;3;Increse rotations, MoveSteering, OnForRotations, Rotations = 5, Speed = 75, Steering = 0, MotorPorts = 123;
### 2018_galilei_1;3;decrease speed, MoveSteering, OnForRotations, Rotations = 5, Speed = 75, Steering = 0, MotorPorts = 123;
### 2018_galilei_1;4;change type OnForSeconds, MoveSteering, OnForSeconds, Seconds = 1, Speed = 75, Steering = 0, MotorPorts = 123;