import streamlit as st
import pandas as pd
import yfinance as yf

file = pd.read_csv('Stocks.csv')

row_1 = st.columns(5)
st.title("Live Stock Data\n")

if "last_symbol" not in st.session_state:
    st.session_state.last_symbol = "AMD"

def call_error():
    with right_col:
        st.error("Error: Enter Correct Name/Symbol")

def fetch_stock(stock_symbol):
    st.session_state.last_symbol = stock_symbol
    with left_col:
        try:
            ticker_symbol = stock_symbol
            ticker_data = yf.Ticker(ticker_symbol)
            ticker_dataframe = ticker_data.history(start='2024-8-14', end='2025-9-18')
            
            live_price = ticker_data.info['regularMarketPrice']
            st.subheader(f"{ticker_symbol} Live Price:")
            st.markdown(f"#### {live_price}$\n")
            
            st.markdown(f"#### {ticker_symbol} Volume:")
            st.line_chart(ticker_dataframe.Volume)
            
            st.markdown(f"#### {ticker_symbol} Closing:")
            st.line_chart(ticker_dataframe.Close)
        except:
            st.error("Cannot fetch details. Error: Incorrect Name/Symbol")

left_col, right_col = st.columns([3, 1])

st.sidebar.title("Crypto Search")
if st.sidebar:
    crypto_search = st.sidebar.text_input("Search Here: ")
    if st.sidebar.button("Search"):
        if crypto_search:
            fetch_stock(crypto_search + '-USD')

with right_col:
    stock_name = st.text_input("Enter Stock Name:")
    search_button = st.button("Check")

with left_col:
    with row_1[0]:
        if st.button("NVIDIA"):
            fetch_stock('NVDA')
    with row_1[1]:
        if st.button("Bitcoin"):
            fetch_stock('BTC-USD')
    with row_1[2]:
        if st.button("Microsoft"):
            fetch_stock('MSFT')
    with row_1[3]:
        if st.button("Apple"):
            fetch_stock('AAPL')
    with row_1[4]:
        if st.button("Google"):
            fetch_stock('GOOGL')

    if search_button:
        if len(stock_name) <= 5:
            if any(char.isupper() for char in stock_name):
                symbol = stock_name
                fetch_stock(stock_symbol=symbol)
            else:
                call_error()
        else:
            query = file.query(f"Keys == '{stock_name}'")
            symbol = query.iloc[0, 1]
            fetch_stock(stock_symbol=symbol)
fetch_stock(st.session_state.last_symbol) # Default Display
