import json, os, urllib

import django
django.setup()

from billcatcher.models import Lawmaker, Vote

url = 'http://www.wral.com/news/state/nccapitol/data_set/14376504/?dsi_id=ncga-eid&version=jsonObj'

def generate_votes():
	text = ['Yea','Nay','NV','Absent']
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	for d in data:
		if d['legiscan_id'] != str(0) and d['legiscan_id'] != '':
			print d['legiscan_id']
			for x in range(1,5):
				Vote.objects.get_or_create(
					vote_id = int(str(d['legiscan_id']) + str(x)),
					member = Lawmaker.objects.get(legiscan_id=d['legiscan_id']),
					vote_code = x,
					vote_text = text[x-1]
					)

if __name__ == '__main__':
	generate_votes()
	print "...votes generated"