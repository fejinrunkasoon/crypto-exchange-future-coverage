import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class HTXFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://api.hbdm.com/linear-swap-api/v1/swap_contract_info'
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for contract in data.get('data', []):
                pair = contract.get('contract_code', '')
                base = contract.get('base_currency', '')
                
                if not base and pair and '-' in pair:
                    parts = pair.split('-')
                    if len(parts) >= 2:
                        base = parts[0]
                
                if pair and base:
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': 'USDT',
                        'type': 'perpetual',
                        'exchange': 'htx'
                    })
                
            logger.info(f"HTX fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"HTX fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'htx'