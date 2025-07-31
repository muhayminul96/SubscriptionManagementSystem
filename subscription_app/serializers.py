from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Plan, Subscription, ExchangeRateLog


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_days']


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'plan_id', 'start_date', 'end_date', 'status', 'created_at']
        read_only_fields = ['start_date', 'end_date', 'created_at']


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateLog
        fields = ['base_currency', 'target_currency', 'rate', 'fetched_at']
