import requests
from bs4 import BeautifulSoup

URL = "https://finance.yahoo.com/quote/MMM"
headers={
        "User-Agent": "Mi navegador 1.0"
}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
valor = soup.find("span", {"data-testid": "qsp-price"})
print(valor.text.strip())
