from tokenize import group
import numpy as np
import pandas as pd
import pm4py
from multiprocessing import Process
import multiprocessing
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness_evaluator
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py.algo.analysis.woflan import algorithm as woflan
import glob
import os

input_path="output_preprocessing_ExB\\change\\*.csv"
output_dir="output_mining_ExB"

def calcola_metriche(net, noise, log, initial_marking, final_marking, return_dict,i):
    metrica={}
    metrica['noise']= round(noise,2)
    metrica['fitness'] = replay_fitness_evaluator.apply(log, net, initial_marking, final_marking, variant=replay_fitness_evaluator.Variants.ALIGNMENT_BASED)["averageFitness"]
    metrica['precision'] = precision_evaluator.apply(log, net, initial_marking, final_marking, variant=precision_evaluator.Variants.ALIGN_ETCONFORMANCE)
    metrica['generalization'] = generalization_evaluator.apply(log, net, initial_marking, final_marking)
    metrica['simplicity'] = simplicity_evaluator.apply(net)
    metrica['is_sound'] = woflan.apply(net, initial_marking, final_marking, parameters={woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True,
                                                    woflan.Parameters.PRINT_DIAGNOSTICS: False,
                                                    woflan.Parameters.RETURN_DIAGNOSTICS: False})
    return_dict[i]= metrica
    

if __name__ == '__main__':
      
    for filename in glob.glob(input_path):
        
        event_log = pd.read_csv(filename, encoding ="utf_8")
        event_log = pm4py.format_dataframe(event_log, case_id='Case_Id',timestamp_key='Timestamp',activity_key='Activity')
        start_activty = pm4py.get_start_activities(event_log)
        end_activity = pm4py.get_end_activities(event_log)
        
        group_name=filename.split("\\")[-1].split(".")[0]
        
        #scrittura file xes     
        os.makedirs(output_dir, exist_ok=True) 
        filename_xes=output_dir+"/"+group_name+".xes"
        pm4py.write_xes(event_log, filename_xes)
        log = pm4py.read_xes(filename_xes) 

        nets=[]
        im=[]
        fm=[]
        number_step=9        
        for i in range (0,number_step,1):
            noise=i/10+0.1
            #applico l'algoritmo inductive miner con i diversi noise threshold
            net, initial_marking, final_marking = inductive_miner.apply(log, variant=inductive_miner.Variants.IMf, 
                                                                        parameters={inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD: noise})
            nets.insert(i,net)
            im.insert(i,initial_marking)
            fm.insert(i,final_marking)
            path=output_dir+"/images_net/"+group_name
            os.makedirs(path, exist_ok=True)         
            path+="/noise "+str(round(noise,2)).replace(".",",") +".png"
            #salvataggio immagine rete di petri sul percorso definito            
            pm4py.save_vis_petri_net(nets[i], initial_marking, final_marking, path)    
        
        '''
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p=[]
        #eseguo un thread per il calcolo delle metriche per ogni step di noise threshold
        for i in range (0,number_step,1):  
            p.insert(i, Process(target=calcola_metriche, args=(nets[i],i/10+0.1, log, im[i], fm[i], return_dict, i)))
            p[i].start()         
        
        #attendo che i vari thread terminino    
        for i in range (0,9,1):       
            p[i].join()       
        
        #scrittura metriche ottenute in file di output csv
        pd.DataFrame(return_dict.values()).to_csv(output_dir+"/metriche_"+group_name+".csv", header=True, index=False)
        '''        

