import requests
import logging
from typing import List, Dict
from .base import BaseFetcher
from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class HyperliquidFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            url = 'https://api.hyperliquid.xyz/info'
            headers = {'Content-Type': 'application/json'}
            payload = {"type": "meta"}
            response = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            for coin in data.get('universe', []):
                pair = f"{coin['name']}-USDC"
                result.append({
                    'market_key': pair,
                    'base': coin['name'],
                    'quote': 'USDC',
                    'type': 'perpetual',
                    'exchange': 'hyperliquid'
                })
                
            logger.info(f"Hyperliquid fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"Hyperliquid fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'hyperliquid'