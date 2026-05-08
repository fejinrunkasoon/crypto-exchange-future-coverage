import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class DeribitFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            currencies = ['BTC', 'ETH']
            
            for currency in currencies:
                url = 'https://www.deribit.com/api/v2/public/get_instruments'
                params = {'currency': currency, 'kind': 'future'}
                response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                
                data = response.json()
                for inst in data.get('result', []):
                    if 'PERPETUAL' in inst['instrument_name']:
                        pair = inst['instrument_name']
                        base = inst['base_currency']
                        quote = 'USDT'
                        result.append({
                            'market_key': pair,
                            'base': base,
                            'quote': quote,
                            'type': 'perpetual',
                            'exchange': 'deribit'
                        })
                
            logger.info(f"Deribit fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"Deribit fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'deribit'