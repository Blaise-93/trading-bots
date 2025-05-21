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


class BotCreateRequest(BaseModel):
    '''Bot creation request schema for data validation'''
    name: str
    strategy: str
    base_order_size: float
    safety_order_size: float
    account_id: int
    pairs: list
    base_order_volume: int
    take_profit: float
    safety_order_volume: float
    martingale_volume_coefficient: float
    martingale_step_coefficient: float
    max_safety_orders: int
    active_safety_orders_count: int
    safety_order_step_percentage: float
    take_profit_type: str
