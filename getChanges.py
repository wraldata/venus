'''
getChanges.py
A python script (version 2.0 of get_new_bills.py) to download a new Master File from the Legiscan API and check
against our application's existing master file for any bill changes.
Currently checks for old file in data/master_file_old.json

We periodically need to update with new session dates

Usage:
python getChanges.py
'''

import json
import urllib.request
import datetime, os
from os import listdir
from os.path import isfile, join

#API key for your Legiscan account (contained in gitignored directory)
legiscan_key = open('./keys/.legiscan_key','r').read().rstrip('\n')

#open a log for writing
master_log = open('master_log.txt', 'a')

#function to get session ids
def get_sessionList():
	session_url = 'https://api.legiscan.com/?key=' + legiscan_key + '&op=getSessionList&state=NC'
	session_list = []
	try:
		print('[api call]: ' + str(session_url))
		session_data = urllib.request.urlopen(session_url).read()
		session_json = json.loads(session_data)
		for session in session_json['sessions']:
			#Capturing all sessions from 2021 on
			if session['year_start'] >= 2021:
				session_list.append(session['session_id'])
	except Exception as e:
		print('ERROR: Something went wrong with retrieving the sessionList at ' + str(datetime.datetime.now()) + ' ' + str(e))
	return session_list

#define function to get master lists with specificed session ids
def get_masters(session_list):
	base_url = 'https://api.legiscan.com/?key=' + legiscan_key + '&op=getMasterList&id='
	url_list = []
	session_bills = {}
	counter = 0
	#get session ids and build list of urls
	for session in session_list:
		master_url = base_url + str(session)
		url_list.append(master_url)
	#read in master list with each session id
	for url in url_list:
		#open the url and load in the json
		print('[api call]: ' + str(url))
		current_session = json.loads(urllib.request.urlopen(url).read())
		for item in current_session['masterlist']:
			if item != 'session':
				#append to master list object
				session_bills[counter] = current_session['masterlist'][item]
				counter += 1
	#save to master_file.json
	try:
		with open('data/master_file.json','w') as change_file:
			json.dump(session_bills,change_file)
		master_log.write('SUCCESS: Newest master file saved at ' + str(datetime.datetime.now()) + '\n')
	except:
		master_log.write('ERROR: Invalid master file URL recorded at ' + str(datetime.datetime.now()) + '\n')
		return

#define function to get new bills and overwrite old ones
def get_bill_updates():
	#open the new file
	with open('data/master_file.json') as data_file:
		master_data = json.load(data_file)

	#open the old file
	#need to build in exception for if it doesn't exist
	if (os.path.isfile('data/master_file_old.json')):
		with open('data/master_file_old.json') as old_file:
			old_data = json.load(old_file)
	else:
		master_log.write('ALERT: No master file detected. Starting new one.\n')
		old_data = 0;

	#initialize the counters
	change_count = 0
	unchanged_count = 0
	undled_count = 0
	#create empty list to store bills
	changed_bills = []
	unchanged_bills = []
	undled_bills = []

	dl_bills = [f.split('.')[0] for f in listdir('data/bills/') if isfile(join('data/bills/', f))]
	dl_rollcalls = [f.split('.')[0] for f in listdir('data/votes/') if isfile(join('data/votes/', f))]

	for item in master_data:
		#check for a blank file
		if(old_data == 0):
			change_count += 1
			changed_bills.append(item)
		#otherwise go through the old file and compare
		else:
			try:
				#check for altered change_hash
				if (master_data[item]['change_hash'] != old_data[item]['change_hash']):
					change_count += 1
					changed_bills.append(item)
				else:
					unchanged_count += 1
					unchanged_bills.append(item)
			#if it throws a key error, the bill is new, so add it
			except KeyError:
				change_count += 1
				changed_bills.append(item)
		#check on our undownloaded bills...
		if(str(master_data[item]['bill_id']) not in dl_bills):
			undled_count += 1
			undled_bills.append(item)
	master_log.write('ALERT: ' + str(unchanged_count) + ' bills have stayed the same in Legiscan data\n')
	master_log.write('ALERT: ' + str(change_count) + ' bills have been updated in Legiscan data\n')
	master_log.write('ALERT: ' + str(undled_count) + ' bills have not been downloaded yet\n')
	for bill in changed_bills:
		get_bill(master_data[bill]['bill_id'],master_data[bill]['number'])
		get_rollcall(master_data[bill]['bill_id'])
	#temporary maintenance steps that should normally be disabled
	#for bill in undled_bills:
	#	get_bill(master_data[bill]['bill_id'],master_data[bill]['number'])
	#	get_rollcall(master_data[bill]['bill_id'])
	#delete this after maintencance
	#for bill in unchanged_bills:
	#	get_rollcall(master_data[bill]['bill_id'])

#function to get a specific bill, by defined id
def get_bill(bill_id, name):
	bill_url = 'https://api.legiscan.com/?key=' + legiscan_key + '&op=getBill&id=' + str(bill_id)

	try:
		print('[api call]: ' + str(bill_url))
		bill_file = urllib.request.urlopen(bill_url).read()
		f = open('data/bills/' + str(bill_id) + '.json', 'wb')
		f.write(bill_file)
		f.close()
		master_log.write(name + ' data saved at ' + str(datetime.datetime.now()) + '\n')
	except:
		master_log.write('ERROR: Invalid bill file URL\n')
		return

#function to get role call details, by defined id
def get_rollcall(bill_id):
	#open downloaded bill json given bill_id
	with open('data/bills/' + str(bill_id) + '.json') as bill_file:
		bill_data = json.load(bill_file)
	#define rollcall list variable
	rollcall_list = []
	#store rollcall ids in list from bill votes
	for vote in bill_data['bill']['votes']:
		rollcall_list.append(vote['roll_call_id'])
	for rollcall_id in rollcall_list:
		#check if rollcall json already exists
		if (os.path.isfile('data/votes/' + str(rollcall_id) + '.json')):
			master_log.write('Rollcall ' + str(rollcall_id) + ' exists. Skipped.\n')
			#if not, then download it
		else:
			rollcall_url = 'https://api.legiscan.com/?key=' + legiscan_key + '&op=getRollCall&id=' + str(rollcall_id)
			#rollcall_file = urllib.request.URLopener()
			try:
				print('[api call]: ' + str(rollcall_url))
				#rollcall_file.retrieve(rollcall_url,'data/votes/' + str(rollcall_id) + '.json')
				rollcall_file = urllib.request.urlopen(rollcall_url).read()
				f = open('data/votes/' + str(rollcall_id) + '.json', 'wb')
				f.write(rollcall_file)
				f.close()
				master_log.write('Rollcall ' + str(rollcall_id) + ' saved at ' + str(datetime.datetime.now()) + '\n')
			except:
				master_log.write('ERROR: Invalid rollcall file URL\n')
				return

if __name__ == '__main__':
	#run the functions
	get_masters(get_sessionList())
	get_bill_updates()
	master_log.write('Finished at ' + str(datetime.datetime.now()) + '\n')
	master_log.write('= = = = = = = = = =\n')

	#now make the file you downloaded the old file
	os.rename('data/master_file.json','data/master_file_old.json')
