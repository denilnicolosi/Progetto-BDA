import pandas as pd
import pm4py

from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness_evaluator
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py.algo.analysis.woflan import algorithm as woflan

file_input="wrong.csv"
event_log = pd.read_csv(file_input, encoding ="utf_8")
event_log = pm4py.format_dataframe(event_log, case_id='Case_Id',timestamp_key='Timestamp',activity_key='Activity')
start_activty = pm4py.get_start_activities(event_log)
end_activity = pm4py.get_end_activities(event_log)
print("Start activities: {}\nEnd activities: {}".format(start_activty, end_activity))

pm4py.write_xes(event_log, "log.xes")
log = pm4py.read_xes('log.xes')

metriche = []

for i in range (1,10,1):
    noise=i/10
    net, initial_marking, final_marking = inductive_miner.apply(log, variant=inductive_miner.Variants.IMf, parameters={inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD: noise})
    
    path="images_net/"+file_input.split(".")[0]+"/step "+str(i)+" noise "+str(round(noise,2)).replace(".",",") +".png"
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, path)    
    
    metrica={}
    metrica['noise']= noise
    metrica['fitness'] = replay_fitness_evaluator.apply(log, net, initial_marking, final_marking, variant=replay_fitness_evaluator.Variants.ALIGNMENT_BASED)["averageFitness"]
    metrica['precision'] = precision_evaluator.apply(log, net, initial_marking, final_marking, variant=precision_evaluator.Variants.ALIGN_ETCONFORMANCE)
    metrica['generalization'] = generalization_evaluator.apply(log, net, initial_marking, final_marking)
    metrica['simplicity'] = simplicity_evaluator.apply(net)
    metrica['is_sound'] = woflan.apply(net, initial_marking, final_marking, parameters={woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True,
                                                    woflan.Parameters.PRINT_DIAGNOSTICS: False,
                                                    woflan.Parameters.RETURN_DIAGNOSTICS: False})
    metriche.append(metrica) 
     

pd.DataFrame(metriche).to_csv("metriche_"+file_input.split(".")[0]+".csv", header=True, index=False)












#dfg, start_activities, end_activities = pm4py.discover_dfg(log)
#pm4py.view_dfg(dfg, start_activities, end_activities)

#process_model = pm4py.discover_bpmn_inductive(log, 0.1)
#pm4py.view_bpmn(process_model)

#process_tree = pm4py.discover_tree_inductive(log)
#pm4py.view_process_tree(process_tree)

#map = pm4py.discover_heuristics_net(log, dependency_threshold=0.9)
#pm4py.view_heuristics_net(map)

#net2, im2, fm2 = pm4py.discover_petri_net_inductive(log, 0.7)

#net2, im2, fm2 = pm4py.discover_petri_net_alpha_plus(log)
#pm4py.view_petri_net(net2, im2, fm2)

#net2, im2, fm2 = pm4py.discover_petri_net_heuristics(log)
#pm4py.view_petri_net(net2, im2, fm2)

