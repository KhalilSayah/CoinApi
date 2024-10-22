import scrapy
import json
import os
import gzip
from datetime import datetime, timedelta

class CoinAPISpider(scrapy.Spider):
    name = "coinapi_spider"

    # Liste de tokens API
    api_tokens = [
        "6A107133-B7DC-496E-84C4-90A0F934EAF7"

    ]

    # Liste des symboles avec date_debut et date_fin
    symbol_id_list = [
        {"symbol_id": "OKEX_PERP_CVC_USDT", "date_debut": "2022-01-01", "date_fin": "2022-02-05"}
    ]

    token_index = 0
    request_count = 0
    max_requests_per_token = 100

    # URL de base
    base_url = "https://rest.coinapi.io/v1/orderbooks/{symbol_id}/history?apikey={apikey}&date={date}&limit=100000"

    def start_requests(self):
        for symbol_data in self.symbol_id_list:
            symbol_id = symbol_data["symbol_id"]
            date_debut = datetime.fromisoformat(symbol_data["date_debut"])
            date_fin = datetime.fromisoformat(symbol_data["date_fin"])

            current_date = date_debut
            while current_date <= date_fin:
                # Générer l'URL de la requête
                api_token = self.api_tokens[self.token_index]
                formatted_date = current_date.isoformat()
                url = self.base_url.format(symbol_id=symbol_id, apikey=api_token, date=formatted_date)

                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={"symbol_id": symbol_id, "date": formatted_date}
                )

                current_date += timedelta(days=1)
                self.request_count += 1

                if self.request_count >= self.max_requests_per_token:
                    self.request_count = 0
                    self.token_index += 1

                    if self.token_index >= len(self.api_tokens):
                        self.token_index = 0
                        self.log("Tous les tokens ont été utilisés, retour au premier.")

    def parse(self, response):
        symbol_id = response.meta["symbol_id"]
        date = response.meta["date"]

        data = response.json()

        date_obj = datetime.fromisoformat(date)
        year = date_obj.year
        month = date_obj.month

        directory_path = f"Data/{symbol_id}/{year}/{month:02d}"

        os.makedirs(directory_path, exist_ok=True)

        file_name = f"{symbol_id}_{date_obj.date()}.json.gz"
        file_path = os.path.join(directory_path, file_name)

        with gzip.open(file_path, 'wt', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        self.log(f"Données stockées et compressées pour {symbol_id} à la date {date} dans {file_path}")