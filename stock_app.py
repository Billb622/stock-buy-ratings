import streamlit as st
import pandas as pd
import finnhub

st.title("📈 Analyst BUY Rating Tracker")

api_key = st.text_input("🔑 Enter your Finnhub API Key:", type="password")
if not api_key:
    st.warning("Please enter your Finnhub API key to begin.")
    st.stop()

finnhub_client = finnhub.Client(api_key=api_key)

ticker_input = st.text_area("📋 Enter stock tickers (comma-separated):", "AAPL, MSFT, NVDA, AMZN, GOOGL, META")
tickers = [t.strip().upper() for t in ticker_input.split(',') if t.strip()]

if st.button("🔍 Get Analyst Ratings"):
    results = []
    with st.spinner("Fetching data..."):
        for ticker in tickers:
            try:
                recs = finnhub_client.recommendation_trends(ticker)
                if recs:
                    latest = recs[0]
                    total_buy = latest['buy'] + latest['strongBuy']
                    results.append({
                        'Ticker': ticker,
                        'Strong Buy': latest['strongBuy'],
                        'Buy': latest['buy'],
                        'Hold': latest['hold'],
                        'Sell': latest['sell'],
                        'Strong Sell': latest['strongSell'],
                        'Total BUY Ratings': total_buy,
                        'Period': latest['period']
                    })
            except Exception as e:
                st.error(f"Error for {ticker}: {e}")

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values(by='Total BUY Ratings', ascending=False).reset_index(drop=True)
        st.success("✅ Results loaded!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="buy_rated_stocks.csv", mime='text/csv')
    else:
        st.warning("No results found.")