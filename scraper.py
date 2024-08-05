import requests
from bs4 import BeautifulSoup
import re

url = 'https://novelmania.com.br/novels/magus-supremo-ms/capitulos/volume-1-capitulo-5'

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

site = requests.get(url, headers=headers)
if site.status_code == 200:
  soup = BeautifulSoup(site.content, 'html.parser')
  box = soup.find('div', class_='text')

  if box:
    title = box.find('h2', class_="mt-0 mb-3 text-center").text
    
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    
    for tag in box(['h3']):
      tag.decompose()

    content = box.text.strip()


    with open(f'{title}.txt', 'w', encoding='utf-8') as file:
      file.write(content)

    print(content)
  else:
    print("Elemento 'box' não encontrado." )
else:
  print(f"Erro ao acessar a página: Status code {site.status_code}")



