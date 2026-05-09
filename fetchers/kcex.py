import json
import logging
from typing import List, Dict
from .base import BaseFetcher

logger = logging.getLogger(__name__)


class KCEXFetcher(BaseFetcher):
    def fetch(self) -> List[Dict]:
        result = []
        try:
            with open('kcex_contract.json', 'r', encoding='utf-8') as f:
                contracts = json.load(f)
            
            for contract in contracts:
                if '_USDT' in contract or '_USDC' in contract:
                    parts = contract.split('_')
                    if len(parts) == 2:
                        base = parts[0]
                        quote = parts[1]
                        result.append({
                            'market_key': contract,
                            'base': base,
                            'quote': quote,
                            'type': 'perpetual',
                            'exchange': 'kcex'
                        })
            
            logger.info(f"KCEX fetch completed: {len(result)} contracts")
        except Exception as e:
            logger.error(f"KCEX fetch failed: {str(e)}")
            
        return result
    
    def get_name(self) -> str:
        return 'kcex'