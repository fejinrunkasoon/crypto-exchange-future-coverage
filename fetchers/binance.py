import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class BinanceFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for symbol in data.get('symbols', []):
                if symbol.get('contractType') == 'PERPETUAL':
                    pair = symbol['symbol']
                    base = pair.replace('USDT', '')
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': 'USDT',
                        'type': 'perpetual',
                        'exchange': 'binance'
                    })
                    
            logger.info(f"Binance fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"Binance fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'binance'