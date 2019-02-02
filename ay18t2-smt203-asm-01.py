########################################################################
# ay18t2-smt203-asm-01
# team members:
# 	1. KHIEW PEI YU
# 	2. HAO BOWEN
########################################################################

import requests
import json
import datetime

########################################################################
# global variables 
########################################################################

my_token = '797824642:AAFJicifpPwaeQ0FpdfliQOoAtoGV_cUISw' # put your secret Telegram token here 
url_base = 'https://api.telegram.org/bot{}/'.format(my_token)

url_busArrival = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2'
# if you read page 6 of the LTA data mall, notice that ALL requests to the data 
# mall must include headers, for example: 
# r = requests.get(url=url_busArrival, headers=headers, params=params)
headers = {
	'AccountKey': 'NMy3IJW0Qq6ZmHW+EMg8/Q==', # enter your account key here (check your email when you sign up in LTA data mall) 
	'accept': 'application/json'
}

chat_id = '797824642' # please type in your Telegram user chat id here  

########################################################################
# Telegram method URLs
########################################################################

url_getUpdates = '{}getupdates'.format(url_base)
url_sendMsg = '{}sendMessage'.format(url_base)

# write your code below
# you may wish to break your code into different functions,
# for readability and modularity (which allows for code reuse)
# some suggested functions are below as a guide; 
# however, you are free to change any of the functions below 

def send_welcome(chat_id):
	# write code here 
	bus_msg = get_busarrival_api(60141)

	return
	
def listen_and_reply(chat_id):
	# write code here 
	return 
	
def compute_busarrival(estimated_arrival):
	"""
	Returning an integer
	-2 means that the bus had just left
	other wise stands for minutes before the next arrival
	"""
	time_diff = ''
	# write code here
	# print('ETA: ' + estimated_arrival)

	# Getting current time
	current_t = datetime.datetime.now()
	# print('CRT: ' + str(current_t))

	# Changing ETA into datetime.datetime form
	est_t = datetime.datetime.strptime(estimated_arrival[:-6], "%Y-%m-%dT%H:%M:%S")
	# print('ETA: ' + str(est_t))

	# calculating estmated time or arrival]
	eta_r = (est_t - current_t)
	# print('DLT: ' + str(eta_r))
	# print(str(eta_r))

	# Hint: you may also want to use try.. except for error handling, if necessary
	# return time_diff
	if str(eta_r)[0] == '-':
  		# -2 means that the bus "should" have passed the bus stop based on the estmated_arrival time
		return -2
	# return estimated arrival time in minutes 
	return (int(str(eta_r)[0]) * 60 + int(str(eta_r)[2 : 4]))

def construct_msg(bus_dict):
	"""returning a message which is designed for Telegram
	In the form of 'bus_No.: eta1 eta2 eta3'
	No.123: Arr   09min 15min 
	No.12:  03min 14min 21min
	No.143: Arr   09min 15min 
	No.12:  03min 14min 21min
	"""
	msg =''
	if bus_dict != {} :
		for bus_No, time_list in bus_dict.items():
			msg += '{:8}'.format('No.' + bus_No + ':') # bus service No.
			for time_min in time_list:
				if time_min == -1 :
					msg += 'N.A.  '
				elif time_min >= 2 :
					msg += '{:0>5}'.format(str(time_min) + 'min') + ' '  # time info
				else:
					msg += '{:6}'.format('Arr')
			msg += '\n'
	else:
		msg = "Too late alr,no bus services avaliable :("
	
	return msg

def get_busarrival_dict(bus_list):
	"""
	Return a dictionary of incoming bus in the following form
	incoming_bus{
		string : [int, int, int],
		'147': [08:31, 14:00, 15:00],
		'857': [-2, 08:00, -1]
	}
	-1 means that there is no further bus service
	-2 means that the bus had just left
	0:34:00 stands for H:MM:SS
	"""
	incoming_bus={}

	for bus in bus_list:  #iterating through every bus that is listed in the array 'Services'
		incoming_bus[bus['ServiceNo']] = [compute_busarrival(bus["NextBus"]['EstimatedArrival'])]
		if bus["NextBus2"]['EstimatedArrival'] != "" :
			incoming_bus[bus['ServiceNo']].append(compute_busarrival(bus["NextBus2"]['EstimatedArrival']))
		else:
			incoming_bus[bus['ServiceNo']].append(-1)
		if bus["NextBus3"]['EstimatedArrival'] != "" :
			incoming_bus[bus['ServiceNo']].append(compute_busarrival(bus["NextBus3"]['EstimatedArrival']))
		else:
			incoming_bus[bus['ServiceNo']].append(-1)
	return (incoming_bus)

def get_busarrival_api(bus_stop_code, bus_svc_no = ''):
	"""returning a message which is designed for Telegram
	with user's input of bus_stop No. and bus_svc No.
	In the form of 'bus_No.: eta1 eta2 eta3'
	No.123: Arr   09min 15min 
	No.12:  03min 14min 21min
	No.143: Arr   09min 15min 
	No.12:  03min 14min 21min
	"""
	msg = ''
	params = {
		'BusStopCode': bus_stop_code,
		'ServiceNo': bus_svc_no
	}

	# Getting bus info from LTA 
	r = requests.get(url=url_busArrival, headers=headers, params=params)

	# Choosing bus services info 
	bus_srvs = get_busarrival_dict(r.json()['Services'])
	# incoming_buses = r.json()['Services']
	# print(json.dumps(incoming_buses, sort_keys=True, indent=4))

	# constructing message designed for Telegram
	msg = construct_msg(bus_srvs)
	# print(msg)
	return msg 
	

# send_welcome(chat_id)	
# listen_and_reply(chat_id)
print(get_busarrival_api(60141))
