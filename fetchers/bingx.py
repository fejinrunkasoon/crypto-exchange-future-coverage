import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class BingXFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://open-api.bingx.com/openApi/swap/v2/quote/contracts'
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for contract in data.get('data', []):
                pair = contract.get('symbol', '')
                base = contract.get('baseAsset', '')
                quote = contract.get('quoteAsset', 'USDT')
                if pair:
                    if not base:
                        base = pair.replace('-USDT', '').replace('USDT', '')
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': quote,
                        'type': 'perpetual',
                        'exchange': 'bingx'
                    })
                
            logger.info(f"BingX fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"BingX fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'bingx'