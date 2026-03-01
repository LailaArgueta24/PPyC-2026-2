import requests
from bs4 import BeautifulSoup

try:
    with open("./wiki.html", "r", encoding="utf-8") as file:
        response = file.read()
    soup = BeautifulSoup(response, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    symbols = []
    for row in table.find_all('tr')[1:]:
            symbols.append(row.find('td').text.strip())
    with open("./symbols.txt", "w", encoding="utf-8") as file:       
            for symbol in symbols:
                file.write(symbol + "\n")
except:
    URL = "https://es.wikipedia.org/wiki/Anexo:Compa%C3%B1%C3%ADas_del_S%26P_500"
    headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    #Request permite hacer peticiones http
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        #open permite r/w archivos
        with open("./wiki.html", "w", encoding="utf-8") as file:
            file.write(response.text)
    else:
        print(f"Error al obtener la página: {response.text}")
