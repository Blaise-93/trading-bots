from typing import List, Optional, Dict
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class TradingBot(Base):
    '''Model to be used to store trading bots for user record purposes
      and monitoring'''
    __tablename__ = 'trading_bot'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    strategy = Column(String)
    base_order_size = Column(Float)
    safety_order_size = Column(Float)
    profit_made = Column(Float, default=0.0)
    account_id = Column(Integer, nullable=True)
    pairs = Column(String, default='BTC_USDT')
    base_order_volume = Column(Integer, nullable=True)
    take_profit = Column(Float, nullable=True)
    safety_order_volume = Column(Float, nullable=True)
    martingale_volume_coefficient = Column(Float,  nullable=True)
    martingale_step_coefficient = Column(Float, nullable=True)
    max_safety_orders = Column(Integer, default=0.0)
    active_safety_orders_count = Column(Integer, default=0)
    safety_order_step_percentage = Column(Float, default=0.0)
    take_profit_type = Column(String, default='percentage')


class StrategyItem(BaseModel):
    strategy: str
    options: Dict


class BotCreateRequest(BaseModel):
    '''Bot creation request schema for data validation'''
    name: str
    account_id: int
    is_enabled: Optional[bool] = False
    max_safety_orders: int
    active_safety_orders_count: int
    pairs: List[str]
    strategy_list: List[StrategyItem]
    close_strategy_list: List[Dict] = []
    safety_strategy_list: List[Dict] = []
    max_active_deals: int
    active_deals_count: int
    take_profit: float
    take_profit_type: str
    base_order_volume: float
    safety_order_volume: float
    safety_order_step_percentage: float
    martingale_volume_coefficient: float
    martingale_step_coefficient: float
    stop_loss_percentage: float
    cooldown: int
    btc_price_limit: float
    strategy: str
    profit_currency: str
    stop_loss_type: str
    safety_order_volume_type: str
    base_order_volume_type: str
    trailing_deviation: Optional[float] = None
