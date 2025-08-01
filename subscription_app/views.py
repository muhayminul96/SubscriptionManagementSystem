import json

from rest_framework import status, generics, viewsets, serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import Plan, Subscription, ExchangeRateLog
from .services import ExchangeRateService
from .serializers import PlanSerializer, SubscriptionSerializer, ExchangeRateSerializer
from django.http import JsonResponse


# API ViewSets
class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing subscription plans"""
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing subscriptions"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return subscriptions for the current user only"""
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print("user")
        """Create subscription with proper validation"""
        plan_id = self.request.data.get('plan_id')
        plan = get_object_or_404(Plan, id=plan_id)

        # Check if user already has an active subscription to this plan
        existing_sub = Subscription.objects.filter(
            user=self.request.user,
            plan=plan,
            status='active'
        ).exists()

        if existing_sub:
            raise serializers.ValidationError(
                'You already have an active subscription to this plan'
            )

        with transaction.atomic():
            serializer.save(user=self.request.user, plan=plan)

    def create(self, request, *args, **kwargs):
        """Custom create method with better response"""
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                'message': 'Subscription created successfully',
                'subscription': response.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a subscription"""
        subscription_id = self.request.data.get('subscription_id')
        print(subscription_id)
        subscription = get_object_or_404(Subscription, pk=subscription_id, user=request.user)
        if not subscription:
            return JsonResponse(
                {'error': 'subscriptions not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        elif subscription.status != 'active':
            return JsonResponse(
                {'error': 'Only active subscriptions can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            subscription.status = 'cancelled'
            subscription.save()

        return Response({
            'message': 'Subscription cancelled successfully',
            'subscription': SubscriptionSerializer(subscription).data
        })


class ExchangeRateAPIView(APIView):
    """API view for fetching exchange rates"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch and return the latest exchange rate"""
        base = request.query_params.get('base', 'USD')
        target = request.query_params.get('target', 'BDT')

        try:
            service = ExchangeRateService()
            # rate_data = service.get_exchange_rate(base, target)
            rate_data = service.get_and_save_rate(base, target)

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


class ExchangeRateLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing exchange rate history"""
    queryset = ExchangeRateLog.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-fetched_at']


# Frontend Class-Based Views
class SubscriptionListView(ListView):
    """Frontend view to display all subscriptions"""
    model = Subscription
    template_name = 'subscriptions/list.html'
    context_object_name = 'subscriptions'
    paginate_by = 20

    def get_queryset(self):
        """Get all subscriptions with related data"""
        return Subscription.objects.select_related('user', 'plan').all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Add extra context for statistics"""
        context = super().get_context_data(**kwargs)

        # Add subscription statistics
        all_subscriptions = Subscription.objects.all()
        context.update({
            'total_subscriptions': all_subscriptions.count(),
            'active_subscriptions': all_subscriptions.filter(status='active').count(),
            'cancelled_subscriptions': all_subscriptions.filter(status='cancelled').count(),
            'expired_subscriptions': all_subscriptions.filter(status='expired').count(),
        })

        return context

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription_api(request):
    subscription_id = request.data.get('subscription_id')
    if not subscription_id:
        return Response({'error': 'subscription_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    subscription = get_object_or_404(Subscription, pk=subscription_id, user=request.user)

    if subscription.status != 'active':
        return Response({'error': 'Only active subscriptions can be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        subscription.status = 'cancelled'
        subscription.save()

    serializer = SubscriptionSerializer(subscription)
    return Response({
        'message': 'Subscription cancelled successfully',
        'subscription': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exchange_rate_view(request):
    base = request.query_params.get('base')
    target = request.query_params.get('target')

    if not base or not target:
        return Response({'error': 'base and target currencies are required'}, status=400)

    # Example API call (use your real API key here)
    url = f"https://v6.exchangerate-api.com/v6/YOUR_API_KEY/pair/{base}/{target}"
    response = requests.get(url)

    if response.status_code != 200:
        return Response({'error': 'Failed to fetch exchange rate'}, status=500)

    data = response.json()
    rate = data.get('conversion_rate')

    if not rate:
        return Response({'error': 'Invalid response from exchange rate API'}, status=500)

    # Log to DB
    ExchangeRateLog.objects.create(
        user=request.user,
        base_currency=base,
        target_currency=target,
        rate=rate
    )

    return Response({
        'base': base,
        'target': target,
        'rate': rate
    }, status=200)



# Legacy Function-Based Views for backward compatibility
def subscribe(request):
    """Redirect to ViewSet-based API"""
    return JsonResponse({'message': 'Use /api/subscriptions/ endpoint'}, status=status.HTTP_301_MOVED_PERMANENTLY)


def list_subscriptions(request):
    """Redirect to ViewSet-based API"""
    return JsonResponse({'message': 'Use /api/subscriptions/ endpoint'}, status=status.HTTP_301_MOVED_PERMANENTLY)

@csrf_exempt
def cancel_subscription(request):
    return JsonResponse({'message': 'Use /api/subscriptions/{plan_id}/cancel/ endpoint'},
                    status=status.HTTP_301_MOVED_PERMANENTLY)


def get_exchange_rate(request):
    """Redirect to Class-based API"""
    return JsonResponse({'message': 'Use /api/exchange-rate/ endpoint'}, status=status.HTTP_301_MOVED_PERMANENTLY)


def subscriptions_list(request):
    """Redirect to Class-based view"""
    return SubscriptionListView.as_view()(request)
