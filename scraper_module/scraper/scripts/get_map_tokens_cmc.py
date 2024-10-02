from typing import Dict, List
import requests
from pydantic import BaseModel # type: ignore
from dotenv import load_dotenv # type: ignore
import os

class ApiResponseMapping(BaseModel):
    """Model for API response mapping"""
    data : List
    status : Dict

class TokenInfo(BaseModel):
    id : int
    rank : int
    name : str
    symbol : str
    slug : str

class TokensMapping(BaseModel):
    tokens : List[TokenInfo]


def get_maping(listing_status="active",start=1,limit=100,sort="id",)->ApiResponseMapping:
    load_dotenv()
    api_link = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"

    params = {
        "listing_status" : listing_status,
        "start" : start,
        "limit" : limit,
        "sort" : sort,
    }


    headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': os.getenv("cmc_token_api"),
  }
    r = requests.get(url=api_link,params=params,headers=headers)

    return ApiResponseMapping.parse_obj(r.json())


def get_tokens_maping(response: ApiResponseMapping)->TokensMapping:
    tokens_mapping = TokensMapping(tokens=[])
    for token in response.data:
        tokens_mapping.tokens.append(
            TokenInfo(
                id=token["id"],
                rank=token["rank"],
                name=token["name"],
                symbol=token["symbol"],
                slug=token["slug"],
            )
        )
    return tokens_mapping


def main():
    # Load environment variables from .env file
  load_dotenv()
  # Get mapping
  response = get_maping()
  # Get tokens mapping
  tokens_mapping = get_tokens_maping(response)
  # Print tokens mapping
  print(tokens_mapping)

if __name__ == "__main__":
    main()
