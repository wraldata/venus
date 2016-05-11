'''
getChanges.py
A python script (version 2.0 of get_new_bills.py) to download a new Master File from the Legiscan API and check 
against our application's existing master file for any bill changes.
Currently checks for old file in data/master_file_old.json

Usage:
python getChanges.py
'''

import urllib, json
import datetime, os

#API key for your Legiscan account (contained in gitignored directory)
legiscan_key = open('./keys/.legiscan_key','r').read()

#ncleg.net url format
#will need to update for current year
ncleg_bill = 'http://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?Session=2015&BillID='

#open a log for writing
master_log = open('master_log.txt', 'a')

#function to get session ids
def get_sessionList():
	session_url = 'https://api.legiscan.com/?key=' + legiscan_key + '&op=getSessionList&state=NC'
	session_list = []
	try:
		session_data = urllib.urlopen(session_url).read()
		session_json = json.loads(session_data)
		for session in session_json['sessions']:
			if session['year_start'] == 2015 or session['year_end'] == 2016:
				session_list.append(session['session_id'])
	except:
		print 'ERROR: Something went wrong with retrieving the sessionList at ' + str(datetime.datetime.now())
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
		current_session = json.loads(urllib.urlopen(url).read())
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
	with open('data/master_file_old.json') as old_file:
		old_data = json.load(old_file)

	#initialize the counter
	change_count = 0
	#create empty list to store bills
	changed_bills = []

	for item in master_data:
		try:
			#check for altered change_hash
			if (master_data[item]['change_hash'] != old_data[item]['change_hash']):
				change_count += 1
				changed_bills.append(item)
		#if it throws a key error, the bill is new, so add it
		except KeyError:
			change_count += 1
			changed_bills.append(item)
	master_log.write('ALERT: ' + str(change_count) + ' bills have been updated\n')
	for bill in changed_bills:
		get_bill(master_data[bill]['bill_id'],master_data[bill]['number'])
		get_rollcall(master_data[bill]['number'])

#function to get a specific bill, by defined id
def get_bill(bill_id, name):
	bill_url = 'https://api.legiscan.com/?key=' + legiscan_key + '&op=getBill&id=' + str(bill_id)
	bill_file = urllib.URLopener()
	try:
		bill_file.retrieve(bill_url, 'data/bills/' + name + '.json')
		master_log.write(name + ' data saved at ' + str(datetime.datetime.now()) + '\n')
	except:
		master_log.write('ERROR: Invalid bill file URL\n')
		return

#function to get role call details, by defined id
def get_rollcall(bill_name):
	#open downloaded bill json given bill_name
	with open('data/bills/' + bill_name + '.json') as bill_file:
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
			rollcall_file = urllib.URLopener()
			try:
				rollcall_file.retrieve(rollcall_url,'data/votes/' + str(rollcall_id) + '.json')
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
