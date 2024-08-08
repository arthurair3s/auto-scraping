import requests
from bs4 import BeautifulSoup
import re

# Formatação da URL, cabeçalhos e requisição HTTP
url = f'https://centralnovel.com/supreme-magus-prologo-1/'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

def nextpage(soup):
    #procura o botão para a próxima pagina
    pages = soup.find('a', {'rel': 'next'})
    if pages:
        prox_page = pages['href']
        return prox_page
    else:
        return 'error'
while True:
  site = requests.get(url, headers=headers)

  if site.status_code == 200:
    soup = BeautifulSoup(site.content, 'html.parser')
    box = soup.find('div', class_='epcontent entry-content')

    if box:
      title = box.find('div', class_="cat-series").text
      title = re.sub(r'[\\/*?:"<>|]', "", title)




  url = nextpage(soup)

  if not url:
    break

  print(url)




