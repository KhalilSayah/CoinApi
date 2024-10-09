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

class AllocationItem(BaseModel):
    label : str
    value : float

class TokenAllocations(BaseModel):
    allocations : List[AllocationItem]
class AmountAllocations(BaseModel):
    day : str  # Number of days from start_date
    value : float

class AllocationScheduelItem(BaseModel):
    label : str | None
    unlockDescription : str| None
    total_count : float| None
    total_raised : float| None
    vesting_mode : str| None
    byday : List[AmountAllocations]


class TokenReleaseScheduel(BaseModel):
    start_date : str
    allocations_scheduel: List[AllocationScheduelItem]

    @classmethod
    def from_json(cls, data: List[dict],start_date: str):
        """
        Class method to create an instance of TokenReleaseScheduel from JSON data.
        """
        allocations_scheduel = [
            AllocationScheduelItem(
                label=item["tokenName"],
                unlockDescription=item["tokenDescription"],
                total_count=item["totalCount"],
                total_raised=item["totalRaised"],
                vesting_mode=item["vestingMode"]["mode"],
                byday=[
                    AmountAllocations(day=day, value=value) for day, value in item["byDay"].items()
                ]
            )
            for item in data
        ]
        return cls(allocations_scheduel=allocations_scheduel, start_date=start_date)
class TokenMarketData(BaseModel):
    circulating_supply : float
    locked_supply : float
    total_supply : float


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

