from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from .models import Plan, Subscription, ExchangeRateLog
from .serializers import PlanSerializer, SubscriptionSerializer, ExchangeRateSerializer


# API Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe(request):
    try:
        plan_id = request.data.get('plan_id')
        plan = get_object_or_404(Plan, id=plan_id)

        # Check if user already has an active subscription to this plan
        existing_sub = Subscription.objects.filter(
            user=request.user,
            plan=plan,
            status='active'
        ).first()

        if existing_sub:
            return Response(
                {'error': 'You already have an active subscription to this plan'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            subscription = Subscription.objects.create(
                user=request.user,
                plan=plan
            )

        serializer = SubscriptionSerializer(subscription)
        return Response({
            'message': 'Subscription created successfully',
            'subscription': serializer.data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_subscriptions(request):
    """List all subscriptions of the logged-in user"""
    subscriptions = Subscription.objects.filter(user=request.user)
    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response({
        'subscriptions': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    """Cancel a subscription"""
    try:
        subscription_id = request.data.get('subscription_id')
        subscription = get_object_or_404(
            Subscription,
            id=subscription_id,
            user=request.user
        )

        if subscription.status != 'active':
            return Response(
                {'error': 'Only active subscriptions can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            subscription.status = 'cancelled'
            subscription.save()

        return Response({
            'message': 'Subscription cancelled successfully'
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exchange_rate(request):
    """Fetch and return the latest exchange rate"""
    base = request.GET.get('base', 'USD')
    target = request.GET.get('target', 'BDT')

    try:
        service = ExchangeRateService()
        rate_data = service.get_exchange_rate(base, target)

        return Response({
            'base_currency': base,
            'target_currency': target,
            'rate': rate_data['rate'],
            'fetched_at': rate_data['fetched_at']
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )



