from fastapi import FastAPI, Depends, status, HTTPException
from logging import getLogger
from pathlib import Path
import requests
from endpoints import (
    API_KEY, BASE_URL,
    LIVE_ACCOUNT_ID,
    PAPER_ACCOUNT_ID
)
from celery_worker import check_bot_status
from sqlalchemy.orm import Session
from models import TradingBot, BotCreateRequest
from database import get_db

logging = getLogger('fastapi')

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title='Trading Bot',
    description='This is my trading bot DCA strategy API docs assignment',
    version='1.0.0'

)


@app.get('/account')
def starting_point():
    ''' Root of the project for testing purpose'''

    return {'message': 'Welcome to the 3Commas Trading Bot API'}


@app.post("/create-bot", status_code=status.HTTP_201_CREATED)
def create_bot(db: Session = Depends(get_db)):
    """
    Creates a trading bot using the 3Commas API and saves it in the database.

    Args:
        request (BotCreateRequest): Request body with bot details.

    Returns:
        dict: API response stored in the database.
    """
    # Call 3Commas API
    url = f"{BASE_URL}/ver1/bots/create_bot"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    # For dynamic rendering,
    #  We can use basemodel, Botcreaterequest class for this
    payload = {
        "name": "Test Bot",
        "account_id": PAPER_ACCOUNT_ID,
        "pairs": ["BTC_USDT"],
        "strategy": "dca",
        "base_order_volume": 10,
        "take_profit": 1.5,
        "safety_order_volume": 5,
        "martingale_volume_coefficient": 1.05,
        "martingale_step_coefficient": 1.02,
        "max_safety_orders": 3,
        "active_safety_orders_count": 1,
        "safety_order_step_percentage": 2.0,
        "take_profit_type": "percentage"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        if response.status_code == 200:
            try:
                bot_data = response.json()
            except requests.exceptions.JSONDecodeError:
                return {"error": "Failed to decode JSON response",
                        "details": response.text}
            bot = TradingBot(
                id=bot_data.get("id"),
                name=bot_data.get("name"),
                strategy=bot_data.get("strategy"),
                base_order_size=bot_data.get("base_order_size"),
                safety_order_size=bot_data.get("safety_order_size"),
                profit_made=bot_data.get("profit", 0.0)
            )

            db.add(bot)
            db.commit()
            db.refresh(bot)

            return {"message": "Bot created successfully", "bot": bot_data}
        else:
            return {"error": "Failed to create bot",
                    "details": response.json()}
    except Exception as e:
        logging.error(f'Error occured: {e}')


@app.get('/bot-status/{bot_id}')
def get_bot_status(bot_id: int):
    '''Endpoint to retrieve bot status using celery as a background task
    which invariably automate the process.

    Args:
        bot_id (int): The bot ID to check

    Returns:
        dict: Task ID for tracking status

    '''
    task = check_bot_status(bot_id)
    logging.info(f'Task ID: {task.id} status intiated successfully')
    return {'task_id': task.id, 'status': 'Bot status check initiated'}


@app.get('/bot/{bot_id}')
def get_bot(bot_id: int, db: Session = Depends(get_db)):
    '''Retrieve bot data and profits'''

    bot = db.query(TradingBot).filter(TradingBot.id == bot_id).first()
    if not bot:
        return {'message': 'Bot not found'}
    return {'bot': bot}


@app.get('/update_profit/{bot_id}')
def update_profit(bot_id: int, profit: float, db: Session = Depends(get_db)):
    '''Update profits made after the trade is completed by the user.'''

    bot = db.query(TradingBot).filter(TradingBot.id == bot_id).first()
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {bot_id} not found')
    bot.profit_made += profit
    db.commit()
    logging.info(f'Profit made on this bot id: {bot_id}')
    return {'message': 'Profit updated', 'bot':  bot}
