'''
get_new_bills.py
A python script to download a new Master File from the Legiscan API and check 
against our application's existing master file for any bill changes.
Currently checks for old file in data/master_file_old.json
Usage:
python get_new_bills.py
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

#grab the most recent master file from legiscan
def get_master():
	master_url = 'https://api.legiscan.com/?key=' + legiscan_key + '&op=getMasterList&state=NC'
	master_file = urllib.URLopener()
	try:
		master_file.retrieve(master_url, 'data/master_file.json')
		master_log.write('SUCCESS: Newest master file saved at ' + str(datetime.datetime.now()) + '\n')
	except:
		master_log.write('ERROR: Invalid master file URL recorded at ' + str(datetime.datetime.now()) + '\n')
		return

#check the change hash in the legiscan master file for any updated/newly introduced bills
def get_updated_bills():
	#open the new file
	with open('data/master_file.json') as data_file:
		master_data = json.load(data_file)
	#get the status of the json; run if OK
	if master_data['status'] == 'OK':
		master_log.write('JSON status OK at ' + str(datetime.datetime.now()) + '\n')

		#open the old file
		#need to build in exception for if it doesn't exist
		with open('data/master_file_old.json') as old_file:
			old_data = json.load(old_file)

		#initialize the counter
		change_count = 0
		#create empty list to store bills
		changed_bills = []

		for new_item in master_data['masterlist']:
			#don't count the 'session' id or you get a key error
			#ignores old entries that don't appear in the new file
			if new_item != 'session':
				try:
					#check for altered change_hash
					if (master_data['masterlist'][new_item]['change_hash'] != old_data['masterlist'][new_item]['change_hash']):
						change_count += 1
						changed_bills.append(new_item)
				except KeyError:
					change_count += 1
					changed_bills.append(new_item)
		master_log.write('ALERT: ' + str(change_count) + ' bills have been updated\n')
		for bill in changed_bills:
			get_bill(master_data['masterlist'][bill]['bill_id'],master_data['masterlist'][bill]['number'])
			get_rollcall(master_data['masterlist'][bill]['number'])
	else:
		master_log.write('JSON status ERROR at ' + str(datetime.datetime.now()) + '\n')

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
	get_master()
	get_updated_bills()
	master_log.write('Finished at ' + str(datetime.datetime.now()) + '\n')
	master_log.write('= = = = = = = = = =\n')

	#now make the file you downloaded the old file
	os.rename('data/master_file.json','data/master_file_old.json')
