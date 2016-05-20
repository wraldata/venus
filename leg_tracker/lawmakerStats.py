'''
lawmakerStats.py
A python script to store a json file containing various statistical calculations for lawmakers

usage:
export DJANGO_SETTINGS_MODULE=leg_tracker.settings
python lawmakerStats.py

By Tyler Dukes, WRAL
'''

import json, os, urllib, re

import django
django.setup()

#load your models
from billcatcher.models import Lawmaker, Party

lawmaker_url = 'http://52.22.90.29/lawmakers/?format=json'
#for testing
#rollcall_url = 'http://52.22.90.29/rollcalls/?format=json&bill_identifier=3540'
rollcall_url = 'http://52.22.90.29/rollcalls/?format=json'

#global variables to be used in other calculations
dem_missed = []
gop_missed = []
dem_loyalty = []
gop_loyalty = []

def calc_votes():
	#load lawmaker data
	lawmaker_response = urllib.urlopen(lawmaker_url)
	lawmaker_data = json.loads(lawmaker_response.read())
	dem_list = []
	gop_list = []
	dem_record = {}
	gop_record = {}

	#create array of dem lawmakers and gop lawmakers
	for lawmaker in lawmaker_data:
		if lawmaker['party'] == "D":
			dem_list.append(lawmaker['url'])
		elif lawmaker['party'] == "R":
			gop_list.append(lawmaker['url'])

	print "...lawmakers loaded and filed"

	#load all rollcall votes
	rollcall_response = urllib.urlopen(rollcall_url)
	rollcall_data = json.loads(rollcall_response.read())

	print "...rollcall data loaded"

	#for each vote:
	#calculate majority vote of dems
	#calculate majority vote of gop
	for vote in rollcall_data:
		#blank array tracks number of Yea, Nay, NV, Absent
		#codes correspond to 1, 2, 3, 4 defined in the vote file
		dem_votes = [0,0,0,0]
		gop_votes = [0,0,0,0]
		for v in vote['votes']:
			if v['member'] in dem_list:
				dem_votes[v['vote_code']-1] += 1
			elif v['member'] in gop_list:
				gop_votes[v['vote_code']-1] += 1
		#calculate majority vote and add to dem_record
		if dem_votes[0] > dem_votes[1]:
			dem_record[vote['url']] = 1
		elif dem_votes[1] > dem_votes[0]:
			dem_record[vote['url']] = 2
		else:
			dem_record[vote['url']] = 0
		#calculate majority vote and add to gop_record
		if gop_votes[0] > gop_votes[1]:
			gop_record[vote['url']] = 1
		elif gop_votes[1] > gop_votes[0]:
			gop_record[vote['url']] = 2
		else:
			gop_record[vote['url']] = 0

	#for each lawmaker
	for lawmaker in lawmaker_data:
		#initialize variables for each lawmaker
		total_votes = 0;
		party_votes = 0;
		missed_votes = 0;
		vote_opps = 0;
		for vote in rollcall_data:
			for v in vote['votes']:
				if lawmaker['url'] == v['member']:
					#calculate total votes, votes w/party, rate
					if v['vote_code'] == 1 or v['vote_code'] == 2:
						vote_opps += 1
						total_votes += 1
						current_vote = v['vote_code']
						if lawmaker['party'] == "D":
							if current_vote == dem_record[vote['url']]:
								party_votes += 1
						elif lawmaker['party'] == "R":
							if current_vote == gop_record[vote['url']]:
								party_votes += 1
					#calculate missed or "not voting"
					elif v['vote_code'] == 3 or v['vote_code'] == 4:
						vote_opps += 1
						missed_votes += 1
		print lawmaker['name'] + " votes: " + str(party_votes) + "/" + str(total_votes)
		print lawmaker['name'] + " missed votes: " + str(missed_votes) + "/" + str(vote_opps)
		
		#add calculated values to dem/gop array so we can calculate party info later
		if lawmaker['party'] == "D":
			dem_missed.append(party_votes/total_votes)
			dem_loyalty.append(missed_votes/vote_opps)
		elif lawmaker['party'] == "R":
			gop_missed.append(party_votes/total_votes)
			gop_loyalty.append(missed_votes/vote_opps)

		#provide values to update
		updated_values = {
			'total_votes' : total_votes,
			'party_votes' : party_votes,
			'missed_votes' : missed_votes,
			'vote_opportunities' : vote_opps
		}
		#create a new lawmaker called _ to refer to it later
		#if it exists, update it with the new information
		pk_id = lawmaker['url'].split('/')[-2]
		_, created = Lawmaker.objects.update_or_create(
			legiscan_id = pk_id,
			defaults = updated_values
		)
	print dem_loyalty
	print dem_missed
	dem_values = {
		'loyalty_avg' : calc_average(dem_loyalty),
		'missed_avg' : calc_average(dem_missed)
	}
	print dem_values['loyalty_avg']
	print dem_values['missed_avg']
	gop_values = {
		'loyalty_avg' : calc_average(gop_loyalty),
		'missed_avg' : calc_average(gop_missed)
	}
	print gop_values['loyalty_avg']
	print gop_values['missed_avg']
	_, created = Party.objects.update_or_create(
		party_id = 0,
		defaults = gop_values
	)
	_, created = Party.objects.update_or_create(
		party_id = 1,
		defaults = dem_values
	)

def calc_average(values):
	total = 0
	count = 0
	for value in values:
		total += value
		count += 1
	return total/count

if __name__ == '__main__':
	calc_votes()
	print "...lawmakers stats updated"