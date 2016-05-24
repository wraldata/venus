# loadBills.py v2.0
# Takes a directory of json files in ../data/bills/ and imports them into
# billcatcher django app.
#
# usage:
# export DJANGO_SETTINGS_MODULE=leg_tracker.settings
# python loadBills.py
#
# todo:
# - Could we make it skip bills that haven't changed to save on time/server usage?
# By Tyler Dukes, WRAL

import json, os, datetime
#Fixes datetimefield runtime warning
import warnings
#added the following lines to cope with model not loading error
#solved here: http://stackoverflow.com/a/25244833
import django
django.setup()

#load your models
from billcatcher.models import Bill, Lawmaker

bill_directory = '../data/bills/'
all_bills = os.listdir(bill_directory)
summary_base = 'http://www.ncleg.net/gascripts/billsummaries/billsummaries.pl?Session=2015&BillID='
master_log = open('../master_log.txt', 'a')

def load_bills(file_name):
	sponsor_names = []
	with open(file_name) as f:
		data = json.load(f)

		#iterate through the json to catch the file date
		acting_chamber = ''
		for index, entry in enumerate(data['bill']['history']):
			if entry['action'] == 'Filed':
				date = entry['date']
			if index+1 == len(data['bill']['history']):
				if entry['chamber'] == 'H':
					acting_chamber = "House: "
				elif entry['chamber'] == 'S':
					acting_chamber = "Senate: "
				last_action = acting_chamber + entry['action']
				action_date = entry['date']

		#store all the sponsor lawmaker objects in an array
		for sponsor in data['bill']['sponsors']:
			if sponsor['sponsor_type_id'] == 1:
				try:
					sponsor_names.append(Lawmaker.objects.get(legiscan_id=sponsor['people_id']))
				except:
					master_log.write("Error: The lawmaker " + sponsor['name'] + "'s ID not found at " + str(datetime.datetime.now()) + "\n")

		#create a new bill called _ to refer to it later
		#if it exists, update it with the new information
		#clear out the sponsors to allow us to load most recent version
		updated_values = {
			'state_link' : data['bill']['state_link'],
			'bill_number' : data['bill']['bill_number'],
			'title' : data['bill']['title'],
			'description' : data['bill']['description'],
			'file_date' : date,
			'bill_summaries' : summary_base + data['bill']['bill_number'],
			'last_action' : last_action,
			'last_action_date' : action_date,
			'sponsors':'[]',
		}
		try:
			_, created = Bill.objects.update_or_create(
				bill_id = data['bill']['bill_id'],
				defaults = updated_values
			)
		except:
			print 'Error on :',data['bill']['bill_id'],updated_values
		if created == True:
			master_log.write('Bill created from ' + file_name + ' at ' + str(datetime.datetime.now()) + '\n')
		else:
			master_log.write('Bill updated from ' + file_name + ' at ' + str(datetime.datetime.now()) + '\n')
		#iterate through sponsor_names and add each Lawmaker object to the sponsors ManyToManyField
		for name in sponsor_names:
			_.sponsors.add(name)

if __name__ == '__main__':
	master_log.write('Loading bills at ' + str(datetime.datetime.now()) + '\n')
	for bill in all_bills:
		#only grab the file if it's a json
		if bill[-5:] == '.json':
			with warnings.catch_warnings():
				warnings.simplefilter("ignore")
				load_bills(bill_directory + bill)
	master_log.write('All bills loaded at ' + str(datetime.datetime.now()) + '\n')