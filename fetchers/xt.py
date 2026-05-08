import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class XTFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://fapi.xt.com/future/market/v1/public/symbol/list'
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            contracts = data.get('result', [])
            for contract in contracts:
                pair = contract.get('symbol', '')
                base = contract.get('baseCoin', '')
                quote = contract.get('quoteCoin', 'USDT')
                if pair:
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': quote,
                        'type': 'perpetual',
                        'exchange': 'xt'
                    })
                
            logger.info(f"XT.COM fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"XT.COM fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'xt'