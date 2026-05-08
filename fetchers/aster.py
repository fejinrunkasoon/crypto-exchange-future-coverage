import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class AsterFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        urls_to_try = [
            'https://api.aster.exchange/api/v1/public/markets',
            'https://api.asterprotocol.io/v1/markets',
        ]
        
        for url in urls_to_try:
            try:
                response = requests.get(url, timeout=REQUEST_TIMEOUT, verify=False)
                response.raise_for_status()
                
                data = response.json()
                if 'data' in data:
                    markets = data['data']
                elif 'result' in data:
                    markets = data['result']
                elif isinstance(data, list):
                    markets = data
                else:
                    markets = []
                
                for market in markets:
                    pair = market.get('symbol', '')
                    base = market.get('baseCurrency', market.get('base', ''))
                    quote = market.get('quoteCurrency', market.get('quote', 'USDT'))
                    if pair:
                        result.append({
                            'market_key': pair,
                            'base': base,
                            'quote': quote,
                            'type': 'perpetual',
                            'exchange': 'aster'
                        })
                
                if result:
                    break
                    
            except Exception as e:
                logger.debug(f"ASTER fetch failed for {url}: {str(e)}")
                continue
        
        logger.info(f"ASTER fetch completed: {len(result)} contracts")
        return result
    
    def get_name(self) -> str:
        return 'aster'