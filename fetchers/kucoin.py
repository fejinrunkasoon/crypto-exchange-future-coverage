import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class KuCoinFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://api-futures.kucoin.com/api/v1/contracts/active'
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for contract in data.get('data', []):
                pair = contract.get('symbol', '')
                base = contract.get('baseCurrency', '')
                quote = contract.get('quoteCurrency', '')
                if base and quote:
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': quote,
                        'type': 'perpetual',
                        'exchange': 'kucoin'
                    })
                
            logger.info(f"KuCoin fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"KuCoin fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'kucoin'