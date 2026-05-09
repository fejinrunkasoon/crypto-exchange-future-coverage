from typing import List, Dict, Set
import pandas as pd

ASSET_MAPPING = {
    'XBT': 'BTC',
    'XBTUSD': 'BTC',
    'BTCC': 'BTC',
}

def normalize_base(base: str) -> str:
    if not base:
        return ''
    normalized = base.upper().strip()
    normalized = normalized.replace('1000000', '')
    normalized = ASSET_MAPPING.get(normalized, normalized)
    return normalized

def normalize_market_key(market_key: str) -> str:
    normalized = market_key.upper().strip()
    normalized = normalized.replace('-', '').replace('_', '').replace('/', '')
    normalized = normalized.replace('PERP', '').replace('SWAP', '').replace('USDT', '')
    normalized = normalized.replace('USDC', '').replace('USD', '')
    normalized = normalized.replace('PF_', '')
    normalized = ASSET_MAPPING.get(normalized, normalized)
    return normalized.strip()


def analyze_contracts(data: List[Dict]) -> Dict:
    df = pd.DataFrame(data)
    
    df['normalized_market'] = df['market_key'].apply(normalize_market_key)
    df['normalized_base'] = df['base'].apply(normalize_base)
    
    exchange_contract_counts = df.groupby('exchange').size().to_dict()
    exchange_base_counts = df.groupby('exchange')['normalized_base'].nunique().to_dict()
    
    markets_by_exchange = {}
    for exchange in df['exchange'].unique():
        markets_by_exchange[exchange] = set(df[df['exchange'] == exchange]['normalized_market'])
    
    if len(markets_by_exchange) > 0:
        common_markets = set.intersection(*markets_by_exchange.values())
    else:
        common_markets = set()
    
    market_exchange_count = {}
    for market in df['normalized_market'].unique():
        exchanges_with_market = df[df['normalized_market'] == market]['exchange'].unique()
        market_exchange_count[market] = len(exchanges_with_market)
    
    unique_markets_by_exchange = {}
    for exchange, markets in markets_by_exchange.items():
        other_markets = set()
        for other_exchange, other_mkts in markets_by_exchange.items():
            if other_exchange != exchange:
                other_markets.update(other_mkts)
        unique_markets_by_exchange[exchange] = markets - other_markets
    
    base_by_exchange = {}
    for exchange in df['exchange'].unique():
        base_by_exchange[exchange] = set(df[df['exchange'] == exchange]['normalized_base'])
    
    common_bases = set.intersection(*base_by_exchange.values()) if base_by_exchange else set()
    
    unique_bases_by_exchange = {}
    for exchange, bases in base_by_exchange.items():
        other_bases = set()
        for other_exchange, other_bs in base_by_exchange.items():
            if other_exchange != exchange:
                other_bases.update(other_bs)
        unique_bases_by_exchange[exchange] = bases - other_bases
    
    base_coverage = df.groupby('normalized_base')['exchange'].nunique().sort_values(ascending=False).to_dict()
    
    exchange_list = list(markets_by_exchange.keys())
    
    partial_common_bases = {}
    for base, count in base_coverage.items():
        if count > 1 and count < len(exchange_list):
            exchanges_with_base = df[df['normalized_base'] == base]['exchange'].unique()
            partial_common_bases[base] = {
                'count': count,
                'exchanges': exchanges_with_base
            }
    
    heatmap_data = []
    for i, ex1 in enumerate(exchange_list):
        row = []
        for j, ex2 in enumerate(exchange_list):
            common = len(markets_by_exchange[ex1] & markets_by_exchange[ex2])
            row.append(common)
        heatmap_data.append(row)
    
    overlap_analysis = {}
    for exchange, markets in markets_by_exchange.items():
        all_common = len(markets & common_markets)
        partial_common = 0
        unique = len(unique_markets_by_exchange[exchange])
        
        for market in markets:
            if market not in common_markets and market_exchange_count[market] > 1:
                partial_common += 1
        
        overlap_analysis[exchange] = {
            'all_common': all_common,
            'partial_common': partial_common,
            'unique': unique
        }
    
    return {
        'df': df,
        'exchange_contract_counts': exchange_contract_counts,
        'exchange_base_counts': exchange_base_counts,
        'common_markets': common_markets,
        'market_exchange_count': market_exchange_count,
        'unique_markets_by_exchange': unique_markets_by_exchange,
        'common_bases': common_bases,
        'unique_bases_by_exchange': unique_bases_by_exchange,
        'base_coverage': base_coverage,
        'partial_common_bases': partial_common_bases,
        'heatmap_data': heatmap_data,
        'exchange_list': exchange_list,
        'overlap_analysis': overlap_analysis
    }