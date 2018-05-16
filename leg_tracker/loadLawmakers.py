#This script will be periodically run to load in lawmakers to the leg_tracker system.
#Probably need to think through the workflow
#When is this run? Automatically or manually?
#Do we keep lawmakers in the database if they're no longer active?
#maybe with the active boolean?
#
#
# usage:
# export DJANGO_SETTINGS_MODULE=leg_tracker.settings
# python loadLawmakers.py
#
# By Tyler Dukes, WRAL

import json, os, urllib, sys

from billcatcher.models import Lawmaker

url = 'http://www.wral.com/news/state/nccapitol/data_set/14376504/?dsi_id=ncga-eid&version=jsonObj'

def load_lawmakers():
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	for d in data:
		if d['legiscan_id'] != str(0) and d['legiscan_id'] != '':
			print d['legiscan_id']
			try:
				Lawmaker.objects.get_or_create(
					name = d['member'],
					party = d['party'],
					position = d['title'],
					member_id = d['ncleg_id'],
					headshot = 'https://wral.com' + d['headshot'],
					district = d['district'],
					county_short = d['county_short'],
					phone = d['phone'],
					email = d['email'],
					county_long = d['county_long'],
					chamber = d['chamber'],
					legiscan_id = d['legiscan_id'],
					eid = d['eid'],
					active = str(1)
					)
			except:
				print "Unexpected error:",d['member'],sys.exc_info()[0]

if __name__ == '__main__':
	load_lawmakers()
	print "...lawmakers loaded"