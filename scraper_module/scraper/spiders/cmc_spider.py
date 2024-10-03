import json
from scraper.scripts.get_map_tokens_cmc import get_maping, get_tokens_maping
from ..items import ApiResponseItem, ApiResponseStatus, PriceDataPoint, TokenPrice, TokenPriceDetails
import scrapy


class CMCSpider(scrapy.Spider):
    name = "CMC_Spider"
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

    def start_requests(self):
        api_response = get_maping()
        tokens_mapping = get_tokens_maping(api_response)
        for token in tokens_mapping.tokens:
            yield scrapy.Request(
                url=f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={token.id}&range=ALL",
                callback=self.parse,
                headers={
                    'User-Agent': self.custom_user_agent
                },
                meta={'token_info': token}
            )

    def parse(self, response):
        response_json = response.json()
        token = response.meta['token_info']
        response_status = ApiResponseStatus.parse_obj(response_json["status"])
        data_points = response_json["data"]["points"]
        price_data_points = []

        for timestamp, point in data_points.items():
            v_list = point['v']
            token_price_details = TokenPriceDetails(
                price=v_list[0],           # price
                volume=v_list[1],          # volume
                market_cap=v_list[2],      # market_cap
                price_in_btc=v_list[3],    # price_in_btc
                circulating_supply=v_list[4]  # circulating_supply
            )

            price_data_point = PriceDataPoint(
                    timestamp=timestamp,
                    item=token_price_details
            )
            price_data_points.append(price_data_point)

        token_price = TokenPrice(
            price_data=price_data_points
        )


        yield ApiResponseItem(
            item_id=token.id,
            token_info = token,
            status =response_status,
            data=token_price
        )