########################################################################
# ay18t2-smt203-asm-01
# team members:
# 	1.
# 	2. 
########################################################################

import requests
import json
import datetime, time 

########################################################################
# global variables 
########################################################################

my_token = '' # put your secret Telegram token here 
url_base = 'https://api.telegram.org/bot{}/'.format(my_token)

url_busArrival = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2'
# if you read page 6 of the LTA data mall, notice that ALL requests to the data 
# mall must include headers, for example: 
# r = requests.get(url=url_busArrival, headers=headers, params=params)
headers = {
	'AccountKey': '', # enter your account key here (check your email when you sign up in LTA data mall) 
	'accept': 'application/json'
}

chat_id = '' # please type in your Telegram user chat id here  

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
	return 
	
def compute_busarrival(estimated_arrival):
	time_diff = ''
	# write code here
	# Hint: you may also want to use try.. except for error handling, if necessary
	return time_diff

def get_busarrival_api(bus_stop_code):
	msg = ''
	# write code here
	return msg 
	
def listen_and_reply(chat_id):
	# write code here 
	return 

send_welcome(chat_id)	
listen_and_reply(chat_id)