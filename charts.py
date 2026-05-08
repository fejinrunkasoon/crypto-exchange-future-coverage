import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List
from config import EXCHANGE_NAMES, EXCHANGE_COLORS


def create_contract_count_chart(exchange_contract_counts: Dict) -> go.Figure:
    df = pd.DataFrame({
        'exchange': [EXCHANGE_NAMES.get(k, k) for k in exchange_contract_counts.keys()],
        'count': list(exchange_contract_counts.values()),
        'color': [EXCHANGE_COLORS.get(k, '#1f77b4') for k in exchange_contract_counts.keys()]
    }).sort_values('count', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=df['count'],
        y=df['exchange'],
        orientation='h',
        marker=dict(color=df['color']),
        text=df['count'],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='各交易所合约数量对比',
        xaxis_title='合约数量',
        yaxis_title='交易所',
        height=400
    )
    
    return fig


def create_heatmap(exchange_list: List, heatmap_data: List[List[int]]) -> go.Figure:
    exchange_names = [EXCHANGE_NAMES.get(e, e) for e in exchange_list]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=exchange_names,
        y=exchange_names,
        colorscale='Blues',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='交易所共同覆盖热力图',
        xaxis_title='交易所',
        yaxis_title='交易所',
        height=500
    )
    
    return fig


def create_overlap_chart(overlap_analysis: Dict) -> go.Figure:
    df = pd.DataFrame(overlap_analysis).T.reset_index()
    df.columns = ['exchange', 'all_common', 'partial_common', 'unique']
    df['exchange'] = df['exchange'].apply(lambda x: EXCHANGE_NAMES.get(x, x))
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['exchange'],
        y=df['all_common'],
        name='所有交易所共有',
        marker_color='blue'
    ))
    
    fig.add_trace(go.Bar(
        x=df['exchange'],
        y=df['partial_common'],
        name='部分交易所共有',
        marker_color='green'
    ))
    
    fig.add_trace(go.Bar(
        x=df['exchange'],
        y=df['unique'],
        name='本交易所独有',
        marker_color='orange'
    ))
    
    fig.update_layout(
        title='交易所覆盖重叠分析',
        xaxis_title='交易所',
        yaxis_title='资产数量',
        barmode='stack',
        height=400
    )
    
    return fig


def create_base_coverage_chart(base_coverage: Dict, filter_type: str = 'all') -> go.Figure:
    df = pd.DataFrame({
        'base': list(base_coverage.keys()),
        'coverage': list(base_coverage.values())
    })
    
    if filter_type == 'all_common':
        df = df[df['coverage'] == max(base_coverage.values())]
    elif filter_type == 'unique':
        df = df[df['coverage'] == 1]
    
    df = df.sort_values('coverage', ascending=True).head(50)
    
    fig = go.Figure(go.Bar(
        x=df['coverage'],
        y=df['base'],
        orientation='h',
        marker=dict(color='purple'),
        text=df['coverage'],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='基础资产覆盖率排行 (TOP 50)',
        xaxis_title='覆盖交易所数量',
        yaxis_title='基础资产',
        height=600
    )
    
    return fig