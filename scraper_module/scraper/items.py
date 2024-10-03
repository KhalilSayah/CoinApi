# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from typing import List
from pydantic import BaseModel # type: ignore



class TokenPriceDetails(BaseModel):
    price : float
    volume : float
    market_cap : float
    price_in_btc : float
    circulating_supply : float

class PriceDataPoint(BaseModel):
    timestamp : str
    item: TokenPriceDetails

class TokenPrice(BaseModel):
    price_data : List[PriceDataPoint]

class ApiResponseStatus(BaseModel):
    timestamp : str
    error_code : str
    error_message : str
    elapsed : str
    credit_count : int
class ApiResponseItem(scrapy.Item):
    item_id = scrapy.Field()
    token_info=scrapy.Field()
    status = scrapy.Field()
    data = scrapy.Field()

