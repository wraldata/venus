from django.contrib import admin

# Register your models here.
from .models import Lawmaker
from .models import Bill
from .models import Rollcall
from .models import Vote

class LawmakerAdmin(admin.ModelAdmin):
	list_display = ['name','chamber','party','county_short']
	search_fields = ['name']
	readonly_fields = ('updated',)

class BillAdmin(admin.ModelAdmin):
	list_display = ['title','bill_number','file_date', 'watch']
	search_fields = ['title', 'bill_number']
	list_filter = ['file_date', 'watch']
	readonly_fields = ('updated',)

class RollcallAdmin(admin.ModelAdmin):
	list_display = ['bill_identifier','desc','date','yea','nay','passed']
	search_fields = ['bill_identifier__title','desc']
	list_filter = ['date','passed']
	readonly_fields = ('updated',)

class VoteAdmin(admin.ModelAdmin):
	list_display = ['member','vote_text']

admin.site.register(Lawmaker, LawmakerAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Rollcall, RollcallAdmin)
admin.site.register(Vote, VoteAdmin)