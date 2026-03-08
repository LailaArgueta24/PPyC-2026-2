import time
import random
import requests
import threading
from bs4 import BeautifulSoup
import queue
from sqlalchemy import create_engine, text

user="postgres"
password="supersecret"
host ="localhost"
port="5432"
database="postgres"

cola_procesos = queue.Queue()

def get_connection(user, password, host, port, database):
    return create_engine(
        url="postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
def insert_price(symbol,price):
    with get_connection(user, password, host, port, database).connect() as connector:
         connector.execute(text(f"INSERT INTO inversiones(symbol,price) VALUES ('{symbol}', {price})"))
#        print(peticion.fetchall())
    
def obtener_precio_stock():
    
    while True:
        try:
            symbol = cola_procesos.get_nowait()
        except queue.Empty:
            break
        URL = f"https://finance.yahoo.com/quote/{symbol}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        while True:
            time.sleep(3 * random.random())
            response = requests.get(URL, headers=headers,)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                valor = soup.find("span", {"data-testid": "qsp-price"})
                if valor:
                    #precio = valor.text.strip()
                    precio = float(valor.text.replace(",", ""))
                    insert_price(symbol,precio)
                else:
                    precio = "Privado"
                break
            else:
                continue
        cola_procesos.task_done()

if __name__ == "__main__":
    with open("./symbols.txt", "r") as f:
        lista_symbolos = [line.strip() for line in f if line.strip()]
    threads = []
    
    for symbol in lista_symbolos:
        cola_procesos.put(symbol)
    
    for _ in range(8):
        t = threading.Thread(target = obtener_precio_stock)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()