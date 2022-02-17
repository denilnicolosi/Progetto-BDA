import pandas as pd
import pm4py
import os
#os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz\bin'

event_log = pd.read_csv("output.csv", encoding ="utf_8")
event_log = pm4py.format_dataframe(event_log, case_id='Case_Id',timestamp_key='Timestamp',activity_key='Activity')
start_activty = pm4py.get_start_activities(event_log)
end_activity = pm4py.get_end_activities(event_log)
print("Start activities: {}\nEnd activities: {}".format(start_activty, end_activity))

pm4py.write_xes(event_log, "log.xes")
log = pm4py.read_xes('log.xes')

#dfg, start_activities, end_activities = pm4py.discover_dfg(log)
#pm4py.view_dfg(dfg, start_activities, end_activities)

#process_model = pm4py.discover_bpmn_inductive(log, 0.001)
#pm4py.view_bpmn(process_model)

#process_tree = pm4py.discover_tree_inductive(log)
#pm4py.view_process_tree(process_tree)

map = pm4py.discover_heuristics_net(log, dependency_threshold=0.9)
pm4py.view_heuristics_net(map)

#net2, im2, fm2 = pm4py.discover_petri_net_inductive(log)
#pm4py.view_petri_net(net2, im2, fm2)

#net2, im2, fm2 = pm4py.discover_petri_net_alpha_plus(log)
#pm4py.view_petri_net(net2, im2, fm2)

#net2, im2, fm2 = pm4py.discover_petri_net_heuristics(log)
#pm4py.view_petri_net(net2, im2, fm2)

