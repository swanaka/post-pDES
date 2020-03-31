import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly.io as pio
import csv

import datetime

string_date_2 = '2020/03/12 10:00:00'
init_time = datetime.datetime.strptime(string_date_2, '%Y/%m/%d %H:%M:%S')

with open('0.csv') as f:
    reader = csv.reader(f)
    data_array = [row for row in reader if row != []]

overall_index = 0
task_index = 0
worker_index = 0
component_index = 0
facility_index = 0

for elem in data_array:
    if elem[0] == 'Total Cost':
        overall_index = data_array.index(elem)
    elif elem[0] == 'Gantt chart of each Task':
        task_index = data_array.index(elem)
    elif elem[0] == 'Gantt chart of each Component':
        component_index = data_array.index(elem)
    elif elem[0] == 'Gantt chart of each Worker':
        worker_index = data_array.index(elem)
    elif elem[0] == 'Gantt chart of each Facility':
        facility_index = data_array.index(elem)

print(facility_index)
overall = data_array[overall_index]
gant_task_data = data_array[task_index : component_index]
gant_worker_data = data_array[worker_index:facility_index]
gant_facility_data = data_array[facility_index:]

for elem in gant_task_data:
    print(elem)
df = []
for data in gant_task_data[2:]:
    task_name = data[1]
    start_time = int(data[4])
    start_time_label = (init_time + datetime.timedelta(minutes=start_time)).strftime('%Y-%m-%d %H:%M:%S')
    finish_time = int(data[5]) + 1
    finish_time_label = (init_time + datetime.timedelta(minutes=finish_time)).strftime('%Y-%m-%d %H:%M:%S')
    dict_elem = dict(Task=task_name, Start=start_time_label, Finish=finish_time_label)
    df.append(dict_elem)
print(df[::-1])

title = 'Gantt Chart (Task)'
fig = ff.create_gantt(df[::-1], title=title, showgrid_x=True, showgrid_y=True)
pio.write_image(fig, 'task_gantt.png')

df = []
for data in gant_worker_data[2:]:
    worker_name = data[2]
    data_length = len(data)
    block_num = int((data_length-3) / 2)
    for i in range(0, block_num):
        start_time = int(data[3 + 2*i])
        start_time_label = (init_time + datetime.timedelta(minutes=start_time)).strftime('%Y-%m-%d %H:%M:%S')
        finish_time = int(data[3+ 2*i + 1]) + 1
        finish_time_label = (init_time + datetime.timedelta(minutes=finish_time)).strftime('%Y-%m-%d %H:%M:%S')
        dict_elem = dict(Task=worker_name, Start=start_time_label, Finish=finish_time_label)
        df.append(dict_elem)

title = 'Gantt Chart (Worker)'
fig = ff.create_gantt(df, title=title, showgrid_x=True, showgrid_y=True, group_tasks=True)
pio.write_image(fig, 'worker_gantt.png')

df = []
for data in gant_facility_data[2:]:
    facility_name = data[2]
    data_length = len(data)
    block_num = int((data_length-3) / 2)
    for i in range(0, block_num):
        start_time = int(data[3 + 2*i])
        start_time_label = (init_time + datetime.timedelta(minutes=start_time)).strftime('%Y-%m-%d %H:%M:%S')
        finish_time = int(data[3+ 2*i + 1]) + 1
        finish_time_label = (init_time + datetime.timedelta(minutes=finish_time)).strftime('%Y-%m-%d %H:%M:%S')
        dict_elem = dict(Task=facility_name, Start=start_time_label, Finish=finish_time_label)
        df.append(dict_elem)

title = 'Gantt Chart (Facility)'
fig = ff.create_gantt(df, title=title, showgrid_x=True, showgrid_y=True, group_tasks=True)
pio.write_image(fig, 'facility_gantt.png')