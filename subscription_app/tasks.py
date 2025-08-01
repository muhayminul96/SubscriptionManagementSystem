from celery import shared_task
from .services import ExchangeRateService

@shared_task
def fetch_usd_to_bdt_rate():
    try:
        service = ExchangeRateService()
        data = service.get_and_save_rate('USD', 'BDT')
        print(data)
    except Exception as e:
        print("Error fetching rate:", e)
