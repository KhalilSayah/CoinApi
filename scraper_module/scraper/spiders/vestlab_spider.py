import json
from scraper.scripts.get_symbol_vestelab import get_list_tokens
from scraper.items import AllocationItem, TokenAllocations, TokenMarketData, TokenReleaseScheduel
from scraper.scripts.utilities import format_data
import scrapy

class VestlabSpider(scrapy.Spider):
    name = 'Vestlab_Spider'

    def start_requests(self):
        tokens_path = get_list_tokens()
        for token in tokens_path:
            yield scrapy.Request(
                url = f"https://vestlab.io{token}",
                callback = self.parse,
                meta = {'token': token}
            )

    def parse(self, response):
        token = response.meta['token']
        # Token Supply

        token_supp_table = response.css('table.table')
        Circulating_supply = token_supp_table.css('tr:nth-child(1) td::text').getall()
        Locked_supply = token_supp_table.css('tr:nth-child(2) td::text').getall()
        Total_supply = token_supp_table.css('tr:nth-child(3) td::text').getall()
        allocations= json.loads(response.css('vestlab-chart-allocations::attr(data)').get())
        token_release_scheduel = json.loads(response.css('vestlab-chart-daomaker-vestings::attr(data)').get())
        scheduel_start_date = response.css('vestlab-chart-daomaker-vestings::attr(start)').get()
        try :
            token_market_data = TokenMarketData(
                circulating_supply = format_data(Circulating_supply[2]),
                locked_supply = format_data(Locked_supply[2]),
                total_supply = format_data(Total_supply[2]),
            )
            token_allocations = TokenAllocations(allocations=[AllocationItem(**item) for item in allocations])
            yield {
            'token':token,
            'MarketData':token_market_data,
            'allocation' :token_allocations,
            'token_release_scheduel':TokenReleaseScheduel.from_json(token_release_scheduel,scheduel_start_date)
        }
        except:  # noqa: E722
            yield{
                'token': token,
                'MarketData': 'Not Found',
                'allocation' : 'Not Found'

            }


