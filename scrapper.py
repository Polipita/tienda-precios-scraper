import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import json
from datetime import datetime

ua = UserAgent()
headers = {
    "User-Agent": ua.random
}

data = []
fecha_actual = datetime.now().strftime('%d-%m-%Y')

with open("urls.json", "r") as file:
    urls = json.load(file)


for tienda, categorias in urls.items():
    for categoria, url in categorias.items():
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            productos = soup.find_all("div", class_="Showcase__content")
            print("productos encontrados ", len(productos))
            for producto in productos:
                try:
                    nombre_elemento = producto.find('a',class_="Showcase__name")
                    precio_elemento = producto.find('div', class_="Showcase__salePrice")

                    if nombre_elemento and precio_elemento :
                        nombre = nombre_elemento.get_text(strip=True)
                        precio = precio_elemento.get_text(strip=True)
                        print(nombre , precio)
                        data.append({
                            "Tienda" : tienda,
                            "Categoria": categoria,
                            "Producto" : nombre,
                            "Precio": precio,
                            "Fecha": fecha_actual
                        })
                except Exception as e:
                    print(f"error en {e}")

df = pd.DataFrame(data)
print(df.head(10))

df.to_excel(f'datos-{fecha_actual}.xlsx',index=False)

