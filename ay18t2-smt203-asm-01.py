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
# LTA methord URLs & Headers
########################################################################

url_busArrival = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2'
# if you read page 6 of the LTA data mall, notice that ALL requests to the data 
# mall must include headers, for example: 
# r = requests.get(url=url_busArrival, headers=headers, params=params)
headers = {
	'AccountKey': 'NMy3IJW0Qq6ZmHW+EMg8/Q==', # enter your account key here (check your email when you sign up in LTA data mall) 
	'accept': 'application/json'
}

########################################################################
# Telegram method URLs & info
########################################################################

my_token = '797824642:AAFJicifpPwaeQ0FpdfliQOoAtoGV_cUISw' # put your secret Telegram token here 
url_base = 'https://api.telegram.org/bot{}/'.format(my_token)
chat_id = '797824642' # please type in your Telegram user chat id here  

url_getUpdates = '{}getupdates'.format(url_base)
url_sendMsg = '{}sendMessage'.format(url_base)

# write your code below
# you may wish to break your code into different functions,
# for readability and modularity (which allows for code reuse)
# some suggested functions are below as a guide; 
# however, you are free to change any of the functions below 

########################################################################
# Telegram listen and relpy functions
########################################################################

def send_welcome(chat_id):
	# write code here 
	return

def process_msg(msg_dict):
	"""This function is used to process a 'message' dictionary in the msg_detail 
	and send respond to the user according to 'text' \n This function doesn't return any value
	"""
	# Declaring text content
	text = ['', '']
	msg = ''

	# Geting message details from msg_dict 
	sender_id = msg_dict['from']['id']
	text = msg_dict['text'].split('\n')
	
	# Analysing 'text' content 
	try:
		msg_type = msg_dict['entities'][0]['type'] 
	except KeyError:
		try: 
			msg = get_busarrival_info(text[0], text[1])
		except IndexError:
			msg = get_busarrival_info(text[0]) 

	# constructing parameter for the Telegram API request
	sendMessage_para = {
		'chat_id' : sender_id,
		'text' : msg,
		'parse_mode' : 'HTML'
	}

	r = requests.post(url = url_sendMsg, params = sendMessage_para)

	print(msg)

	return 

def listen_and_record():
	"""Getting update of unread message from Telegram API then process each message. 
	This function also rewrite the 'offset.txt' with the update_id of the latest message
	"""

	# import 'offset' number from 'offset.txt' 
	with open('offset.txt') as f:
		offset_num_origion = int(f.readline())
	offset_num = offset_num_origion

	# constructing parameter for the Telegram API request
	getUpdates_para = {
		'offset' : offset_num,
		'limit' : '',
		'timeout' : '',
		'allowed_updates' : ''
	}

	# Getting response from Telegram API
	r = requests.get(url = url_getUpdates, params = getUpdates_para)
	unread_msg = r.json()['result']

	# Printing Unread messages
	print(json.dumps(unread_msg, sort_keys=True, indent=4))

	# Processing each item in the 'result' 
	for msg_detail in unread_msg:
		# Update latest 'update_id' to offset_num for later use
		if msg_detail['update_id'] >= offset_num :
			offset_num = msg_detail['update_id'] + 1
		# process message
		process_msg(msg_detail['message'])
	
	# writing latest 'update_id' into 'offset.txt'
	if offset_num != offset_num_origion:
		with open('offset.txt', 'w') as f:
			f.write(str(offset_num))

	return 
	
########################################################################
# LTA bus info construction functions 
########################################################################

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
			msg += '<b>' + '{:8}'.format('No.' + bus_No + ':') + '</b>' # bus service No.
			for time_min in time_list:
				if time_min == -1 :
					msg += 'N.A.  '
				elif time_min >= 2 :
					msg += '{:0>5}'.format(str(time_min) + 'min') + ' '  # time info
				else:
					msg += '{:6}'.format('Arr')
			msg += '\n'
	else:
		msg = "Too late, no bus services avaliable for this station :("
	
	return msg

def construct_busarrival_dict(bus_list):
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

def get_busarrival_info(bus_stop_code, bus_svc_no = ''):
	"""returning a message which is designed for Telegram with user's input of  
		bus_stop_code(string), and 
		bus_svc_no(string)
	In the form of: \n
	bus_No: eta1  eta2  eta3  \n
	No.123: Arr   09min 15min \n
	No.12:  03min 14min 21min \n
	No.143: Arr   09min 15min \n
	No.12:  03min 14min 21min \n
	"""
	msg = ''
	params = {
		'BusStopCode': bus_stop_code,
		'ServiceNo': bus_svc_no
	}

	# Getting bus info from LTA 
	r = requests.get(url=url_busArrival, headers=headers, params=params)

	# Choosing bus services info 
	bus_srvs = construct_busarrival_dict(r.json()['Services'])

	# Printing incoming Bus info
	print(json.dumps(r.json(), sort_keys=True, indent=4))

	# constructing message designed for Telegram
	msg = construct_msg(bus_srvs)
	# print(msg)
	return msg 

listen_and_record()

# print(get_busarrival_info(283457))
