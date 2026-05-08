import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class LighterFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        urls_to_try = [
            'https://api.lighter.io/v1/markets',
            'https://api.lighter.xyz/v1/markets',
            'https://api.lighter.finance/v1/markets',
        ]
        
        for url in urls_to_try:
            try:
                response = requests.get(url, timeout=REQUEST_TIMEOUT, verify=False)
                response.raise_for_status()
                
                data = response.json()
                if 'markets' in data:
                    markets = data['markets']
                elif 'data' in data:
                    markets = data['data']
                elif isinstance(data, list):
                    markets = data
                else:
                    markets = []
                
                for market in markets:
                    pair = market.get('symbol', market.get('pair', ''))
                    base = market.get('baseAsset', market.get('base', ''))
                    quote = market.get('quoteAsset', market.get('quote', 'USDT'))
                    if pair:
                        result.append({
                            'market_key': pair,
                            'base': base,
                            'quote': quote,
                            'type': 'perpetual',
                            'exchange': 'lighter'
                        })
                
                if result:
                    break
                    
            except Exception as e:
                logger.debug(f"Lighter fetch failed for {url}: {str(e)}")
                continue
        
        logger.info(f"Lighter fetch completed: {len(result)} contracts")
        return result
    
    def get_name(self) -> str:
        return 'lighter'