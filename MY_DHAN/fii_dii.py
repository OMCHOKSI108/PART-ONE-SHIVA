import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_fii_dii():
    try:
        url = "https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Example: Parse table (adjust based on site structure)
        table = soup.find("table", {"class": "tblList2"})
        rows = table.find_all("tr")[1:3]  # FII and DII rows
        data = []
        for row in rows:
            cols = row.find_all("td")
            name = cols[0].text.strip()
            net = float(cols[4].text.strip().replace(",", ""))
            data.append({"name": name, "net": net})
        
        print("\nFII/DII Insights:")
        for d in data:
            sentiment = "Bullish" if d["net"] > 0 else "Bearish"
            print(f"{d['name']} Net: ₹{d['net']} Cr ({sentiment})")
        
        return data
    except Exception as e:
        print(f"Error fetching FII/DII: {e}")
        return []

if __name__ == "__main__":
    fii_dii_data = fetch_fii_dii()