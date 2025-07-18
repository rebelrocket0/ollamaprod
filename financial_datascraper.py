import requests

def get_nse_price(symbol: str):
    symbol = symbol.upper()
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }


    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers, timeout=5)  # Get cookies
        response = session.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
        
        try:
            data = response.json()
        except ValueError:
            return {"error": "Failed to parse JSON"}

        price_info = data.get("priceInfo", {})
        intraday = price_info.get("intraDayHighLow", {})

        return {
            "symbol": symbol,
            "last_price": price_info.get("lastPrice"),
            "day_high": intraday.get("max"),
            "day_low": intraday.get("min"),
            "open_price": price_info.get("open"),
            "prev_close": price_info.get("previousClose")
        }

    
    except Exception as e:
        return {"error": str(e)}
