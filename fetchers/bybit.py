import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class BybitFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://api.bybit.com/v5/market/instruments-info'
            params = {'category': 'linear'}
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for inst in data.get('result', {}).get('list', []):
                if inst.get('status') == 'Trading':
                    pair = inst['symbol']
                    base = inst['baseCoin']
                    quote = inst['quoteCoin']
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': quote,
                        'type': 'perpetual',
                        'exchange': 'bybit'
                    })
                    
            logger.info(f"Bybit fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"Bybit fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'bybit'