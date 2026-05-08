import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class KrakenFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://futures.kraken.com/derivatives/api/v3/instruments'
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for inst in data.get('instruments', []):
                pair = inst.get('symbol', '')
                inst_type = inst.get('type', '')
                
                if inst_type == 'flexible_futures' and pair:
                    base = pair.replace('PF_', '').replace('USD', '').upper()
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': 'USDT',
                        'type': 'perpetual',
                        'exchange': 'kraken'
                    })
                
            logger.info(f"Kraken fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"Kraken fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'kraken'