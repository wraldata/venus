from rest_framework import viewsets
from django_filters import rest_framework as filters
from billcatcher.models import Bill, Lawmaker, Vote, Rollcall, Party
from billcatcher.serializers import BillSerializer, LawmakerSerializer, VoteSerializer, RollcallSerializer, PartySerializer

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    #setup for filters
    #NOTE: True/False must be in sentence case
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('watch','bill_id','bill_number','sponsors')

class LawmakerViewSet(viewsets.ModelViewSet):
    queryset = Lawmaker.objects.all()
    serializer_class = LawmakerSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

class RollcallViewSet(viewsets.ModelViewSet):
    queryset = Rollcall.objects.all()
    serializer_class = RollcallSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('bill_identifier','rollcall_id','desc','passed')

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
