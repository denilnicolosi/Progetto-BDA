import pandas
import numpy as np
import os
import sys
import glob

result_file_path="y_tesi_completo_exA.csv"
output_dir="output_preprocessing_ExA"
input_path="./ExA/*/*.rtf"


def diff_param(par1,par2):
    name_param=par1.split(" = ")[0]
    val1=par1.split(" = ")[1]
    val2=par2.split(" = ")[1]
    
    try:
        if(float(val1)>float(val2)):
            return "Decrease"+ name_param
        else:
            return "Increase"+ name_param
    except ValueError:
        return "Change"+ name_param
 
def add_tracelist(activity, row):
    global trace_list
    row=group_name+", "+ str(timestamp) + ", " + activity + ", " + ",".join(row)
    trace_list=np.append(trace_list, [row.split(",")],axis=0)

def difference(row1, row2):
    activity=""
    row=""
    global trace_list
    global timestamp
    #if(np.array_equal(row1,row2)):
        #activity = "No action"
        #if row1[0]!="":
        #add_tracelist(activity,row2)
    #else:
    if(row1[0]!=row2[0]):
        if(row2[0]!="" and row1[0]!=""):
            activity = "Change blockname to "+row2[0]
            add_tracelist(activity,row2)
        elif(row1[0]!=""):
            activity = "Delete blockname "+row1[0]
            add_tracelist(activity,row1)
        else:
            activity = "Add blockname "+row2[0]
            add_tracelist(activity,row2)
    else:
        #controllo se non ha il "=", altrimenti non è tipo ma parametro
        if(row1[1]!=row2[1] and str(row2[1]).find('=')<0):                
                activity = "Change type"+row2[1]
                add_tracelist(activity,row2)
        else:                
            if(str(row2[1]).find('=')>0 and row1[1]!=row2[1]):
                activity= diff_param(row1[1],row2[1])
                add_tracelist(activity,row2)                    
            if(row1[2]!=row2[2]):
                activity= diff_param(row1[2],row2[2])
                add_tracelist(activity,row2)
            if(row1[3]!=row2[3]):              
                activity= diff_param(row1[3],row2[3])
                add_tracelist(activity,row2)
            if(row1[4]!=row2[4]):
                activity= diff_param(row1[4],row2[4])
                add_tracelist(activity,row2)
            if(row1[5]!=row2[5]):
                activity= diff_param(row1[5],row2[5])
                add_tracelist(activity,row2)
                    
def diff_param_value(par1,par2):
    try:
        score=20
        if(par1!=par2):
            name_param=par1.split(" = ")[0]
            val1=par1.split(" = ")[1]
            val2=par2.split(" = ")[1]
            
            score-=abs(float(val1)-float(val2))
            if score<0:
                score=0    
        
        return score
    except ValueError:
        return 0      
    except IndexError:
        return 0 
    except :
        return 0        
                  
def find_score(row1, row2):
    score=0
    if(np.array_equal(row1,row2)):
        score=100
    elif row1[0]!=row2[0]: #if blockname change
        if (row1[0]!="" and row2[0]!=""):
            score=1            
        else:
            score=0
    else:                
        score+=10 #perchè il blockname è uguale                     
        #controllo se non ha il "=", altrimenti non è tipo ma parametro
        if(row1[1]==row2[1] and str(row2[1]).find('=')<0):                
            score+=10                    
        if(str(row2[1]).find('=')>0):
            score+=diff_param_value(row1[1],row2[1])                                 
    
        score+=diff_param_value(row1[2],row2[2])                    
        score+=diff_param_value(row1[3],row2[3])    
        score+=diff_param_value(row1[4],row2[4])    
        score+=diff_param_value(row1[5],row2[5])
    return score

trace_list= [["Case_Id","Timestamp","Activity","Blockname","Type","1st-param","2st-param","3st-param","4st-param"]]


for filename in glob.glob(input_path):
    if filename.endswith(".rtf"):
            
        df1 = pandas.read_csv(filename, encoding ="utf_8")                        
        
        group_name=filename.replace("\\","_")
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
            row=df1._get_value(i,0, takeable = True)
            if row=="STOP PROGRAM;":
                attempt= attempt + 1
                index_instruction=0
            else:
                j=0
                for value in df1.iloc[i].values:
                    value=str(value).replace(";","")                        
                    instruction[attempt][index_instruction][j]=value
                    j=j+1  
                index_instruction=index_instruction+1       
                
        timestamp=0 
        #aggiunta di attività iniziale fittizia alla trace list    
        row=group_name+", "+ str(timestamp) + ", " + "START CASE_ID" + ",,,,,,"
        trace_list=np.append(trace_list, [row.split(",")],axis=0)
        
        #aggiungo i primi blocchi            
        for i in range(len(instruction[0])):
            if(instruction[0][i][0]!=""):
                add_tracelist("Add blockname "+instruction[0][i][0],instruction[0][i])
        
        # costruisco l'event log con le differenze tra i tentativi                    
        for i in range(len(instruction)-1): #ciclo sugli attemp               
            timestamp+=1
            score_list=np.empty((len(instruction[i]),len(instruction[i])))
            
            for j in range(len(instruction[i])): #instruction                     
                for k in range(len(instruction[i])): #instruction 
                    #popolo la matrice di punteggi 
                    score_list[j][k]=find_score(instruction[i][j], instruction[i+1][k])                                    
                    #print(score_list[j][k],j,k)
            #print("Score list:\n"+ str(score_list))                       
            list_index=[]       
            for j in range(len(instruction[i])): #instruction      
                #print("Score list:\n"+ str(score_list))    
                #print("Max:",score_list.max())
                max_index=np.where(score_list==score_list.max())    
                #print("Max index:",max_index[0][0],max_index[1][0])
                list_index.append([max_index[0][0],max_index[1][0]])
                score_list[:,max_index[1][0]]=-1
                score_list[max_index[0][0],:]=-1                
                        
            if(not np.array_equal(instruction[i],instruction[i+1])):
                for index in list_index:
                    difference(instruction[i][index[0]],instruction[i+1][index[1]])  
            
                
         #aggiunta di attività finale fittizia alla trace list         
        row=group_name+", "+ str(timestamp) + ", " + "END CASE_ID" + ",,,,,,"
        trace_list=np.append(trace_list, [row.split(",")],axis=0)
        
    
# composizione di diverse trace list in base al fatto che il gruppo abbia raggiunto o meno l'obiettivo, informazione ricavata dal file "y_tesi_completo_ex*"
df_result = pandas.read_csv(result_file_path, encoding ="utf_8")
trace_list_wrong = trace_list_good = [["Case_Id","Timestamp","Activity","Blockname","Type","1st-param","2st-param","3st-param","4st-param"]]
for row in trace_list:
    start_index=row[0].find("_",row[0].index("_")+1)+1
    group_name=row[0][start_index:]
    res=df_result.loc[df_result["ID"]==group_name]    
    if(not res.empty): 
        if(res.Y.values[0]==0):                       
            trace_list_wrong=np.append(trace_list_wrong, [list(row)],axis=0)
        else:
            trace_list_good=np.append(trace_list_good, [list(row)],axis=0)         

#scrittura in output delle diverse trace list
os.makedirs(output_dir, exist_ok=True) 
pandas.DataFrame(trace_list_good).to_csv(output_dir+"/good.csv", header=False, index=False)
pandas.DataFrame(trace_list_wrong).to_csv(output_dir+"/wrong.csv", header=False, index=False)
pandas.DataFrame(trace_list).to_csv(output_dir+"/all.csv", header=False, index=False)    
    
