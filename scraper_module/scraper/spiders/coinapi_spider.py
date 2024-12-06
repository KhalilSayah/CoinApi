import scrapy
import json
import os
import gzip
from datetime import datetime, timedelta

class CoinAPISpider(scrapy.Spider):
    name = "coinapi_spider"

    # Liste de tokens API
    api_tokens = [
        "052DF3E3-4918-4887-9EF7-C3EC64B3785C",
        "60DE1B5E-E4AA-4C89-A9CB-3BA01A68EB2F",
        "7088F67B-9DB9-4215-B7BD-7B2E02BD70CC",
        "DF0C998C-78A7-4C23-A102-CA7758B6B672",
    ]

    # Liste des symboles avec date_debut et date_fin
    symbol_id_list = [
        {"symbol_id": "OKEX_PERP_CVC_USDT", "date_debut": "2022-01-01", "date_fin": "2022-02-05"}
    ]

    token_index = 0
    request_count = 0
    max_requests_per_token = 10000

    # URL de base
    base_url = "https://rest.coinapi.io/v1/orderbooks/{symbol_id}/history?apikey={apikey}&time_start={time_start}&time_end={time_end}&limit=100000"

    def start_requests(self):
        for symbol_data in self.symbol_id_list:
            symbol_id = symbol_data["symbol_id"]
            date_debut = datetime.fromisoformat(symbol_data["date_debut"])
            date_fin = datetime.fromisoformat(symbol_data["date_fin"])

            current_date = date_debut
            while current_date <= date_fin:
                # Loop through each hour of the day
                for hour in range(24):
                    # Generate the start and end times for the hour
                    time_start = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                    time_end = time_start + timedelta(hours=1)

                    api_token = self.api_tokens[self.token_index]
                    url = self.base_url.format(
                        symbol_id=symbol_id,
                        apikey=api_token,
                        time_start=time_start.isoformat(),
                        time_end=time_end.isoformat()
                    )

                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        meta={
                            "symbol_id": symbol_id,
                            "time_start": time_start.isoformat(),
                            "time_end": time_end.isoformat()
                        }
                    )

                    self.request_count += 1

                    # Switch tokens if max requests per token are exceeded
                    if self.request_count >= self.max_requests_per_token:
                        self.request_count = 0
                        self.token_index += 1

                        if self.token_index >= len(self.api_tokens):
                            self.token_index = 0
                            self.log("All tokens have been used, cycling back to the first.")

                # Move to the next day
                current_date += timedelta(days=1)


    def parse(self, response):
        symbol_id = response.meta["symbol_id"]
        date = response.meta["time_start"]

        data = response.json()

        date_obj = datetime.fromisoformat(date)
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        hour = date_obj.hour

        directory_path = f"Data/{symbol_id}/{year}/{month:02d}/{day:02d}"

        os.makedirs(directory_path, exist_ok=True)

        file_name = f"{symbol_id}_{year}_{month:02d}_{day:02d}_{hour}.json.gz"
        file_path = os.path.join(directory_path, file_name)

        with gzip.open(file_path, 'wt', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        self.log(f"Données stockées et compressées pour {symbol_id} à la date {date} dans {file_path}")