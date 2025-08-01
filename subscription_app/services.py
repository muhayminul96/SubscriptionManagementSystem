# services.py
from datetime import datetime
import requests
from django.conf import settings
from .models import ExchangeRateLog

class ExchangeRateService:
    def __init__(self):
        self.api_key = settings.EXCHANGE_API_KEY
        self.base_url = 'https://v6.exchangerate-api.com/v6'

    def get_exchange_rate(self, base, target):
        """Call external API and return rate data"""
        url = f'{self.base_url}/{self.api_key}/pair/{base}/{target}'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception('Failed to fetch exchange rate')

        data = response.json()
        if data.get('result') != 'success':
            raise Exception('Invalid response from exchange API')

        return {
            'rate': data.get('conversion_rate'),
            'fetched_at': datetime.utcnow()
        }

    def get_and_save_rate(self, base, target):
        """Fetch rate and log it to DB"""
        rate_data = self.get_exchange_rate(base, target)

        ExchangeRateLog.objects.create(
            base_currency=base,
            target_currency=target,
            rate=rate_data['rate']
        )

        return rate_data
