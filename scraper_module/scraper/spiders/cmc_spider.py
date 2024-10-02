from scraper.scripts.get_map_tokens_cmc import get_maping, get_tokens_maping
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
                }
            )

    def parse(self, response):
        yield response.json()
