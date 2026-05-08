import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class GateFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://api.gateio.ws/api/v4/futures/usdt/contracts'
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for contract in data:
                pair = contract.get('name', '')
                if '_USDT' in pair:
                    base = pair.replace('_USDT', '')
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': 'USDT',
                        'type': 'perpetual',
                        'exchange': 'gate'
                    })
                
            logger.info(f"Gate.io fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"Gate.io fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'gate'