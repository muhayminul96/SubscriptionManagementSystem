from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'plans', views.PlanViewSet, basename='plan')
router.register(r'subscriptions', views.SubscriptionViewSet, basename='subscription')
router.register(r'exchange-logs', views.ExchangeRateLogViewSet, basename='exchangelog')

urlpatterns = [
    # API endpoints using ViewSets
    path('api/', include(router.urls)),
    path('api/exchange-rate/', views.ExchangeRateAPIView.as_view(), name='api_exchange_rate'),

    # Frontend views using CBVs
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscriptions_list'),

    # Legacy endpoints (for backward compatibility)
    path('api/subscribe/', views.subscribe, name='api_subscribe'),
    path('api/cancel/', views.cancel_subscription_api, name='api_cancel'),
]