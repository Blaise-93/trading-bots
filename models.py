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


class BotCreateRequest(BaseModel):
    name: str
    strategy: str
    base_order_size: float
    safety_order_size: float
