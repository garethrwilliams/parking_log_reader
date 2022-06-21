from datetime import datetime
from math import ceil

file_name = 'parking2.log'
file = open(file_name, 'r') 
parking_log = {}
data_order = ['date', 'type', 'direction']

# Look through each line of the log and extract the data 

for line in file.readlines():

    details = line.split(',')
    details = [x.strip() for x in details]
    # Remove the unique ref
    vehicle_ref = details.pop(1)

    # Retrieve data from log if present else crate map for data 
    vehicle_data = parking_log[vehicle_ref] if vehicle_ref in parking_log else {'IN/OUT': [], 'TOTAL' : []}

    # Build entry/exit data, append to the correct key and update log
    direction_data = {key:value for key, value in zip(data_order, details)}

    if direction_data['direction'] == 'Entry':
        
        vehicle_data['IN/OUT'].append({'IN': direction_data})
        parking_log[vehicle_ref] = vehicle_data

    if direction_data['direction'] == 'Exit':

        event_ref = len(parking_log[vehicle_ref]['IN/OUT']) - 1
        vehicle_data['IN/OUT'][event_ref]['OUT'] = direction_data

        in_time = datetime.strptime(vehicle_data['IN/OUT'][event_ref]['IN']['date'], "%Y-%m-%d %H:%M:%S.%f")
        out_time = datetime.strptime(vehicle_data['IN/OUT'][event_ref]['OUT']['date'], "%Y-%m-%d %H:%M:%S.%f")
        vehicle_data['TOTAL'].append(out_time - in_time)

file.close()
        

def average_time ():
    total_car_time_list = []

    # Iterate through list to remove only car data
    for x in parking_log:
        is_it_a_car = parking_log[x]['IN/OUT'][0]['IN']['type'] == 'Car'

        if len(parking_log[x]['TOTAL']) > 0 and is_it_a_car:
         for y in parking_log[x]['TOTAL']:

            total_car_time_list.append(y.seconds)

    # If there are no cars return error
    if len(total_car_time_list) == 0:
        return print('No cars have entered the carpark')

    # Otherwise return average stay
    average_time = ceil((sum(total_car_time_list) / len(total_car_time_list)) / 60)
    print('The average time a car used the carpark for was {} minutes'.format(average_time))   

def entered_more_than_once ():

    for x in parking_log:
        is_it_a_car = parking_log[x]['IN/OUT'][0]['IN']['type'] == 'Car'

        if len(parking_log[x]['IN/OUT']) > 1 and is_it_a_car:
            print(f"{x} entered the carpark {len(parking_log[x]['IN/OUT'])} times")


average_time(), entered_more_than_once()