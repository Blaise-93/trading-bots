from celery.schedules import crontab
import os
import requests
from celery import Celery
from endpoints import BASE_URL, API_KEY, PAPER_ACCOUNT_ID
from logging import getLogger


logging = getLogger('fastapi')

celery_app = Celery(
    'trading_bot',
    broker=os.getenv('BROKER_URL'),
    backend=os.getenv('BACKEND_URL')
)


@celery_app.task
def check_bot_status(bot_id: int):
    '''Background Celery task to periodically check the status of a bot

      Args:
        bot_id (int): ID of the bot to monitor

      Returns:
        dict : The latest bot status from 3Commas API

    '''
    url = f'{BASE_URL}/ver1/bots/{bot_id}'
    headers = {'Authorization': f'Bearer {API_KEY}'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.error(f'Unkown error occured: {e}')


@celery_app.task
def execute_trade(order_details):
    '''Executes order details trade asynchoronously. '''

    logging.info(f'Trade executed: {order_details}')
    return f'Trade executed: {order_details}'


@celery_app.task
def check_market_conditions():
    """Check market conditions and trigger bot creation"""
    
    response = requests.get(f"{BASE_URL}/ver1/accounts/market_data")
    data = response.json()

    # If price drops more than 5%, trigger bot creation
    if data['BTC_USDT']['price_change'] < -5:
        payload = {
            "name": "Auto Bot",
            "account_id": PAPER_ACCOUNT_ID,
            "is_enabled": False,
            "max_safety_orders": 4,
            "active_safety_orders_count": 1,
            "pairs": ["BTC_USDT"],
            "strategy_list": [{"strategy": "nonstop", "options": {}}],
            "close_strategy_list": [],
            "safety_strategy_list": [],
            "max_active_deals": 1,
            "active_deals_count": 0,
            "take_profit": 2.0,
            "take_profit_type": "total",
            "base_order_volume": 15.0,
            "safety_order_volume": 30.0,
            "safety_order_step_percentage": 1.0,
            "martingale_volume_coefficient": 2.0,
            "martingale_step_coefficient": 4.0,
            "stop_loss_percentage": 0.0,
            "cooldown": 0,
            "btc_price_limit": 0.0,
            "strategy": "long",
            "profit_currency": "quote_currency",
            "stop_loss_type": "stop_loss",
            "safety_order_volume_type": "quote_currency",
            "base_order_volume_type": "quote_currency",
            "trailing_deviation": 0.2
        }

        fastapi_url = "http://localhost:8000/create-bot"
        response = requests.post(fastapi_url, json=payload)

        if response.status_code == 201:
            logging.info("Bot successfully created!")
        else:
            logging.error(f"Failed to create bot: {response.json()}")

    return "Checked market condition"


'''Run scheduler task of check market conditions every 30 mins '''
celery_app.conf.beat_schedule = {
    'check-market-every-30-minutes': {
        'task': 'tasks.check_market_conditions',
        'schedule': crontab(minute='*/30'),
    },
}
