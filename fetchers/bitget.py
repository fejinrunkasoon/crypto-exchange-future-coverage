import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class BitgetFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://api.bitget.com/api/v2/mix/market/contracts'
            params = {'productType': 'USDT-FUTURES'}
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for contract in data.get('data', []):
                pair = contract.get('symbol', '')
                base = contract.get('baseCoin', '')
                quote = contract.get('quoteCoin', 'USDT')
                if pair:
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': quote,
                        'type': 'perpetual',
                        'exchange': 'bitget'
                    })
                
            logger.info(f"Bitget fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"Bitget fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'bitget'