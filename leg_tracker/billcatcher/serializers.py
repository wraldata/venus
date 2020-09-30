from rest_framework import serializers
from billcatcher.models import Bill, Lawmaker, Vote, Rollcall, Party

class LawmakerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lawmaker
        fields = '__all__'

class BillSerializer(serializers.HyperlinkedModelSerializer):
    sponsors = LawmakerSerializer(many=True)
    class Meta:
        model = Bill
        fields = '__all__'

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class RollcallSerializer(serializers.HyperlinkedModelSerializer):
    votes = VoteSerializer(many=True)
    class Meta:
        model = Rollcall
        fields = '__all__'

class PartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

