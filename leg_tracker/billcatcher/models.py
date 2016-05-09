from django.db import models

class Lawmaker(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name
	party = models.CharField(max_length=1)
	position = models.CharField(max_length=20)
	member_id = models.IntegerField(default=0, help_text='ID assigned by ncleg.net.')
	headshot = models.URLField(help_text='URL of current 180x270 headshot.')
	district = models.IntegerField(default=0)
	county_short = models.CharField(max_length=20)
	phone = models.CharField(max_length=15)
	email = models.EmailField()
	county_long = models.CharField(max_length=100)
	chamber = models.CharField(max_length=10)
	eid = models.IntegerField(default=0, help_text='ID assigned by FollowTheMoney (not unique).')
	legiscan_id = models.IntegerField(primary_key=True, help_text='ID assigned by Legiscan (unique).')
	total_votes = models.IntegerField(default=0, help_text='Number of votes cast by this member. Does not include absent or not voting votes.')
	party_votes = models.IntegerField(default=0, help_text="Number of votes that lined up with the majority of this member party.")
	missed_votes = models.IntegerField(default=0, help_text="Number of votes either missed or marked not voting.")
	vote_opportunities = models.IntegerField(default=0, help_text="Number of voting opportunities for this member.")
	active = models.BooleanField(help_text='Indicates whether member is an active legislator.')
	updated = models.DateTimeField(auto_now=True)

class Bill(models.Model):
	sponsors = models.ManyToManyField(Lawmaker,help_text="Primary sponsors only.")
	title = models.CharField(max_length=140,help_text="Defined by Legiscan. Overwritten when changed by lawmakers.")
	def __str__(self):
		return self.title
	bill_id = models.IntegerField(default=0, help_text="Assigned by Legiscan.")
	state_link = models.URLField(default=0)
	bill_summaries = models.URLField(default=0)
	bill_number = models.CharField(max_length=5)
	description = models.CharField(max_length=200, help_text="Initially defined by title. Can be changed by user and won't be overwritten.")
	file_date = models.DateField('date filed')
	updated = models.DateTimeField(auto_now=True)
	last_action = models.CharField(max_length=200)
	last_action_date = models.DateField('last action date')
	watch = models.BooleanField(default=False, help_text="Check to mark bill as notable on profile pages")

class Vote(models.Model):
	vote_id = models.IntegerField(default=0, primary_key=True)
	member = models.ForeignKey(Lawmaker)
	vote_code = models.IntegerField(default=0)
	vote_text = models.CharField(max_length=10)
	def __str__(self):
		return str(self.member) + ': ' + self.vote_text

class Rollcall(models.Model):
	bill_identifier = models.ForeignKey(Bill)
	rollcall_id = models.CharField(max_length=15)
	date = models.DateField('date of vote')
	desc = models.CharField(max_length=100)
	def __str__(self):
		return self.desc
	yea = models.IntegerField(default=0)
	nay = models.IntegerField(default=0)
	not_voting = models.IntegerField(default=0)
	absent = models.IntegerField(default=0)
	passed = models.IntegerField(default=9)
	votes = models.ManyToManyField(Vote)
	updated = models.DateTimeField(auto_now=True)




