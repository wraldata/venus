'''
Utility function to fix rollcall votes
by adding corresponding bill numbers
Need to roll this into loadVotes for simplicity

usage:
export DJANGO_SETTINGS_MODULE=leg_tracker.settings
python updateBillNo.py
'''

import json, os, urllib, re

import django
django.setup()

from billcatcher.models import Bill, Rollcall

rollcall_url = 'http://52.22.90.29/rollcalls/?format=json'

#load all rollcall votes
rollcall_response = urllib.urlopen(rollcall_url)
rollcall_data = json.loads(rollcall_response.read())

#for each vote:
for vote in rollcall_data:
	#get the bill identifier
	bill_url = vote['bill_identifier']
	bill_response = urllib.urlopen(bill_url + '?format=json')
	bill_data = json.loads(bill_response.read())

	print 'Bill number:' + bill_data['bill_number']

	try:
		Rollcall.objects.filter(rollcall_id=vote['rollcall_id']).update(bill_number=bill_data['bill_number'])
	except:
		print 'Error writing rollcall data on',vote['rollcall_id']
