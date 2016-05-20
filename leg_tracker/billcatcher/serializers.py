from rest_framework import serializers
from billcatcher.models import Bill, Lawmaker, Vote, Rollcall, Party

class LawmakerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lawmaker

class BillSerializer(serializers.HyperlinkedModelSerializer):
    sponsors = LawmakerSerializer(many=True)
    class Meta:
        model = Bill

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote

class RollcallSerializer(serializers.HyperlinkedModelSerializer):
	votes = VoteSerializer(many=True)
	class Meta:
		model = Rollcall

class PartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Party

