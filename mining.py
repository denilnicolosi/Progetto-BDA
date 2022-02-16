import pandas as pd
import pm4py

event_log = pd.read_csv("output.csv", encoding ="utf_8")
event_log = pm4py.format_dataframe(event_log, case_id='Case_Id',timestamp_key='Timestamp',activity_key='Activity')
start_activty = pm4py.get_start_activities(event_log)
end_activity = pm4py.get_end_activities(event_log)
print("Start activities: {}\nEnd activities: {}".format(start_activty, end_activity))

pm4py.write_xes(event_log, "log.xes")

log = pm4py.read_xes('log.xes')
process_model = pm4py.discover_bpmn_inductive(log)
pm4py.view_bpmn(process_model)