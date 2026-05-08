import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class OKXFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://www.okx.com/api/v5/public/instruments'
            params = {'instType': 'SWAP'}
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for inst in data.get('data', []):
                pair = inst['instId']
                base = inst.get('baseCcy', '')
                
                if not base:
                    if '-' in pair:
                        parts = pair.split('-')
                        if len(parts) >= 2:
                            base = parts[0]
                
                if base:
                    result.append({
                        'market_key': pair,
                        'base': base,
                        'quote': 'USDT',
                        'type': 'perpetual',
                        'exchange': 'okx'
                    })
                
            logger.info(f"OKX fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"OKX fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'okx'