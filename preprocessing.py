import pandas
import numpy as np


df1 = pandas.read_csv(".//ExA//ExA//grandi//2018_LiceoGalilei1.rtf", encoding ="utf_8")

instruction = np.empty((len(df1),1,6), dtype='U256')
attempt=0
index_instruction=0
for i in range(len(df1)):
    if df1._get_value(i,0, takeable = True)=="STOP PROGRAM;":
        attempt= attempt + 1
        index_instruction=0
    instruction[attempt][index_instruction]=df1.iloc[i].values
    

#instruction.collect(10)        
print(instruction[:10])
#print(list)
#print(df1.head(10))