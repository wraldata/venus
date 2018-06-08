'''
Utility function to fix rollcall votes
by adding corresponding bill numbers
Need to roll this into loadVotes for simplicity

usage:
export DJANGO_SETTINGS_MODULE=leg_tracker.settings
python updateBillNo.py
'''

import json, os, urllib2, re

import django
django.setup()

from billcatcher.models import Bill, Rollcall

rollcall_url = 'http://localhost/rollcalls/?format=json'

#load all rollcall votes
try:
	rollcall_response = urllib2.urlopen(rollcall_url, None, 300)
except urllib2.URLError, e:
	raise Exception("There was an error: %r" % e)

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
