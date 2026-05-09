import streamlit as st
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from fetchers import (
    BinanceFetcher, OKXFetcher, BybitFetcher, GateFetcher, BitgetFetcher,
    KuCoinFetcher, BingXFetcher, XTFetcher, HTXFetcher, KrakenFetcher,
    DeribitFetcher, HyperliquidFetcher, AsterFetcher, LighterFetcher, KCEXFetcher
)
import analyzer
import charts
from config import EXCHANGES, EXCHANGE_NAMES, MAX_WORKERS, CACHE_TTL


def fetch_all_exchanges():
    fetchers = [
        BinanceFetcher(),
        OKXFetcher(),
        BybitFetcher(),
        GateFetcher(),
        BitgetFetcher(),
        KuCoinFetcher(),
        BingXFetcher(),
        XTFetcher(),
        HTXFetcher(),
        KrakenFetcher(),
        DeribitFetcher(),
        HyperliquidFetcher(),
        AsterFetcher(),
        LighterFetcher(),
        KCEXFetcher()
    ]
    
    results = []
    errors = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(f.fetch): f.get_name() for f in fetchers}
        
        for future in futures:
            exchange_name = futures[future]
            try:
                data = future.result()
                if data:
                    results.extend(data)
            except Exception as e:
                errors.append((exchange_name, str(e)))
    
    return results, errors


@st.cache_data(ttl=CACHE_TTL)
def get_analysis_data(_):
    data, errors = fetch_all_exchanges()
    analysis = analyzer.analyze_contracts(data)
    return data, errors, analysis


def main():
    st.set_page_config(page_title='加密货币交易所永续U本位合约覆盖分析', layout='wide')
    
    st.title('加密货币交易所合约覆盖分析')
    
    if 'refresh_key' not in st.session_state:
        st.session_state['refresh_key'] = 0
    
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.caption(f'数据更新时间: {update_time}')
    with col_btn:
        if st.button('🔄 刷新数据'):
            st.session_state['refresh_key'] += 1
            st.cache_data.clear()
            st.rerun()
    
    data, errors, analysis = get_analysis_data(st.session_state.get('refresh_key', 0))
    
    if errors:
        st.warning('以下交易所数据获取失败:')
        for exchange, error in errors:
            st.error(f"- {EXCHANGE_NAMES.get(exchange, exchange)}: {error}")
    
    st.markdown('---')
    st.subheader('总览')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('已分析交易所数量', len(analysis['exchange_list']))
    
    with col2:
        total_markets = len(analysis['market_exchange_count'])
        st.metric('合约总资产数（去重后）', total_markets)
    
    with col3:
        common_bases_count = len(analysis['common_bases'])
        st.metric('所有交易所共同拥有的资产数', common_bases_count)
    
    with col4:
        total_unique = sum(len(v) for v in analysis['unique_markets_by_exchange'].values())
        st.metric('全部独有资产总数', total_unique)
    
    st.markdown('---')
    st.subheader('各交易所合约数量对比')
    st.plotly_chart(charts.create_contract_count_chart(analysis['exchange_contract_counts']), width='stretch')
    
    st.markdown('---')
    st.subheader('交易所共同覆盖热力图')
    st.plotly_chart(charts.create_heatmap(analysis['exchange_list'], analysis['heatmap_data']), width='stretch')
    
    st.markdown('---')
    st.subheader('交易所覆盖重叠分析')
    st.plotly_chart(charts.create_overlap_chart(analysis['overlap_analysis']), width='stretch')
    
    st.markdown('---')
    st.subheader('数据明细')
    
    tab1, tab2, tab3, tab4 = st.tabs(['共同资产列表', '部分共有资产', '独有资产列表', '原始数据'])
    
    with tab1:
        common_df = pd.DataFrame({'base': sorted(list(analysis['common_bases']))})
        st.dataframe(common_df, width='stretch')
        csv = common_df.to_csv(index=False).encode('utf-8')
        st.download_button('📥 下载 CSV', csv, 'common_bases.csv', 'text/csv', key='download_common')
    
    with tab2:
        partial_data = []
        for base, info in sorted(analysis['partial_common_bases'].items(), key=lambda x: x[1]['count'], reverse=True):
            exchange_names = [EXCHANGE_NAMES.get(ex, ex) for ex in info['exchanges']]
            partial_data.append({
                'base': base,
                '覆盖交易所数量': info['count'],
                '覆盖交易所': ', '.join(exchange_names)
            })
        partial_df = pd.DataFrame(partial_data)
        st.dataframe(partial_df, width='stretch')
        csv = partial_df.to_csv(index=False).encode('utf-8')
        st.download_button('📥 下载 CSV', csv, 'partial_common_bases.csv', 'text/csv', key='download_partial')
    
    with tab3:
        selected_exchange = st.selectbox('选择交易所', EXCHANGES, format_func=lambda x: EXCHANGE_NAMES.get(x, x))
        unique_markets = analysis['unique_markets_by_exchange'].get(selected_exchange, set())
        unique_df = pd.DataFrame({'market_key': sorted(list(unique_markets))})
        st.dataframe(unique_df, width='stretch')
        csv = unique_df.to_csv(index=False).encode('utf-8')
        st.download_button('📥 下载 CSV', csv, f'unique_markets_{selected_exchange}.csv', 'text/csv', key='download_unique')
    
    with tab4:
        df = analysis['df']
        st.dataframe(df, width='stretch')
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('📥 下载 CSV', csv, 'raw_data.csv', 'text/csv', key='download_raw')
    
if __name__ == '__main__':
    main()