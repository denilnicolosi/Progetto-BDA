from asyncio.windows_events import NULL
from inspect import isclass, trace
from statistics import mode
import pandas
import numpy as np
import sys
import os

def diff_param(par1,par2):
    name_param=par1.split(" = ")[0]
    val1=par1.split(" = ")[1]
    val2=par2.split(" = ")[1]
    if(isinstance(val1, (int, float)) and isinstance(val2, (int, float))):
        if(float(val1)>float(val2)):
            return "Decrease "+ name_param
        else:
            return "Increase "+ name_param
    else:
        return "Change "+ name_param
  


def difference(row1, row2):
    activity=""
    row=""
    global trace_list
    global timestamp
    if(np.array_equal(row1,row2)):
        activity = "No action"
        row=group_name+", "+ str(timestamp) + ", " + activity + ", " + ",".join(row2)
        trace_list=np.append(trace_list, [row.split(",")],axis=0)
    else:
        if(row1[0]!=row2[0]):
            activity = "Change blockname to "+row2[0]
            row=group_name+", "+ str(timestamp) + ", " + activity + ", " + ",".join(row2)
            trace_list=np.append(trace_list, [row.split(",")],axis=0)
        else:
            if(row1[1]!=row2[1]):
                activity = "Change type"+row2[1]
                row=group_name+", "+ str(timestamp) + ", " + activity + ", " + ",".join(row2)
                trace_list=np.append(trace_list, [row.split(",")],axis=0)
            else:
                if(row1[2]!=row2[2]):
                    activity= diff_param(row1[2],row2[2])
                    row=group_name+", "+ str(timestamp) + ", " + activity + ", " + ",".join(row2)
                    trace_list=np.append(trace_list, [row.split(",")],axis=0)
                if(row1[3]!=row2[3]):              
                    activity= diff_param(row1[3],row2[3])
                    row=group_name+", "+ str(timestamp) + ", " + activity + ", " + ",".join(row2)
                    trace_list=np.append(trace_list, [row.split(",")],axis=0)
                if(row1[4]!=row2[4]):
                    activity= diff_param(row1[4],row2[4])
                    row=group_name+", "+ str(timestamp) + ", " + activity + ", " + ",".join(row2)
                    trace_list=np.append(trace_list, [row.split(",")],axis=0)
                if(row1[5]!=row2[5]):
                    activity= diff_param(row1[5],row2[5])
                    row=group_name+", "+ str(timestamp) + ", " + activity + ", " + ",".join(row2)
                    trace_list=np.append(trace_list, [row.split(",")],axis=0)   
    timestamp= timestamp +1   

file_output="output.csv"
#np.set_printoptions(threshold=sys.maxsize)
directory=".//ExA"
trace_list= [["Case_Id","Timestamp","Activity","Blockname","Type","1st-param","2st-param","3st-param","4st-param"]]
header=True
for file in os.listdir(directory):
    filename=os.fsdecode(file)
    for file2 in os.listdir(directory+"//"+filename):
        if file2.endswith(".rtf"):
            path=directory+"//"+filename+"//"+file2
            df1 = pandas.read_csv(path, encoding ="utf_8")
            group_name=path.replace("//","_")
            group_name=group_name[2:len(group_name)-4]
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
                    j=0
                    for value in df1.iloc[i].values:
                        value=str(value).replace(";","")                        
                        instruction[attempt][index_instruction][j]=value
                        j=j+1
                        
                        
                    #instruction[attempt][index_instruction]=df1.iloc[i].values
                    index_instruction=index_instruction+1       

            timestamp=0
            #aggiungo una riga vuota per forzare la scrittura gia della prima riga
            instruction=np.insert(instruction, 0, ["","","","","",""],axis=0)
            for i in range(total_attempt-1):
                for j in range(len(instruction[i])):
                    difference(instruction[i][j], instruction[i+1][j])                   

            
pandas.DataFrame(trace_list).to_csv(file_output, header=False, index=False)
    
    

### colonne
### caseid; timestamp; activity;Blockname, Type, 1st-param, 2nd-param, 3rd-param, 4th-param 
### 2018_galilei_1;1;Change blockname to moveSteering, MoveSteering, OnForRotations, Rotations = 1, Speed = 100, Steering = 0, MotorPorts = 123; 
### 2018_galilei_1;2;No action, MoveSteering, OnForRotations, Rotations = 1, Speed = 100, Steering = 0, MotorPorts = 123; 
### 2018_galilei_1;3;Increse rotations, MoveSteering, OnForRotations, Rotations = 5, Speed = 75, Steering = 0, MotorPorts = 123;
### 2018_galilei_1;3;decrease speed, MoveSteering, OnForRotations, Rotations = 5, Speed = 75, Steering = 0, MotorPorts = 123;
### 2018_galilei_1;4;change type OnForSeconds, MoveSteering, OnForSeconds, Seconds = 1, Speed = 75, Steering = 0, MotorPorts = 123;