import os
import requests
from celery import Celery
from endpoints import *
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
    url = f'{BASE_URL}/verl/bots/{bot_id}'
    headers = {'Authorization': f'Bearer {API_KEY}'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.warning(f'Unkown error occured: {e}')


@celery_app.task
def execute_trade(order_details):
    '''Executes order details trade asynchoronously. '''

    logging.info(f'Trade executed: {order_details}')
    return f'Trade executed: {order_details}'
