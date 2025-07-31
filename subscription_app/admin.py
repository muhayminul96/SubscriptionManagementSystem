from django.contrib import admin
from .models import Subscription, ExchangeRateLog, Plan
# Register your models here.
@admin.register(ExchangeRateLog)
class ExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ('base_currency', 'target_currency', 'rate', 'fetched_at')
    list_filter = ('fetched_at',)

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name','price_in_usd','duration_days')
    list_filter = ('name',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan', 'user', 'start_date','status')
    list_filter = ('start_date',)