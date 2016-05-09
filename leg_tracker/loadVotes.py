# loadVotes.py v0.1
# Takes a directory of json files in ../data/votes/ and imports them into
# billcatcher django app.
#
# usage:
# export DJANGO_SETTINGS_MODULE=leg_tracker.settings
# python loadVotes.py
#
# By Tyler Dukes, WRAL

import json, os, datetime
#Fixes datetimefield runtime warning
import warnings
#added the following lines to cope with model not loading error
#solved here: http://stackoverflow.com/a/25244833
import django
django.setup()

#load your models
from billcatcher.models import Bill, Rollcall, Vote, Lawmaker

rollcall_directory = '../data/votes/'
all_rollcalls = os.listdir(rollcall_directory)
master_log = open('../master_log.txt', 'a')

def load_rollcalls(rollcall_file):
	vote_ids = []
	with open(rollcall_file) as f:
		data = json.load(f)

		#store all the vote objects in an array
		for votes in data['roll_call']['votes']:
			try:
				vote_ids.append(Vote.objects.get(vote_id=int(str(votes['people_id']) + str(votes['vote_id']))))
			except:
				master_log.write("Error: The vote ID " + str(votes['people_id']) + str(votes['vote_id']) + " not found at " + str(datetime.datetime.now()) + "\n")

		#create a new rollcall called _ to refer to it later
		#if it exists, update it with the new information
		values = {
			'bill_identifier' : Bill.objects.get(bill_id=data['roll_call']['bill_id']),
			'date' : data['roll_call']['date'],
			'desc' : data['roll_call']['desc'],
			'yea' : data['roll_call']['yea'],
			'nay' : data['roll_call']['nay'],
			'not_voting' : data['roll_call']['nv'],
			'absent' : data['roll_call']['absent'],
			'passed' : data['roll_call']['passed'],
		}
		_, created = Rollcall.objects.update_or_create(
			rollcall_id = data['roll_call']['roll_call_id'],
			defaults = values
		)

		if created == True:
			master_log.write('Rollcall created from ' + rollcall_file + ' at ' + str(datetime.datetime.now()) + '\n')
		else:
			master_log.write('Rollcall updated from ' + rollcall_file + ' at ' + str(datetime.datetime.now()) + '\n')
		#iterate through vote_ids and add each vote object to the Rollcall's ManyToManyField
		for vote in vote_ids:
			_.votes.add(vote)

if __name__ == '__main__':
	master_log.write('Loading rollcalls at ' + str(datetime.datetime.now()) + '\n')
	for rollcall in all_rollcalls:
		#only grab the file if it's a json
		if rollcall[-5:] == '.json':
			with warnings.catch_warnings():
				warnings.simplefilter("ignore")
				load_rollcalls(rollcall_directory + rollcall)
	master_log.write('All rollcalls loaded at ' + str(datetime.datetime.now()) + '\n')