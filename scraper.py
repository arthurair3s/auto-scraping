import requests
from bs4 import BeautifulSoup
import re
import os

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
        return None
    
while url:
  site = requests.get(url, headers=headers)

  # Verificando se a requisição foi bem-sucedida
  if site.status_code == 200:
    soup = BeautifulSoup(site.content, 'html.parser')
    box = soup.find('div', class_='epcontent entry-content')

    # Verificação e criação do diretório onde os arquivos serão salvos
    output_dir = f'Supreme Magus'
    if not os.path.exists(output_dir):
          os.makedirs(output_dir)

    # Verificando se o elemento 'box' foi encontrado
    if box:
      # Extração e limpeza do título e remoção de elementos desnecessarios do texto
      title_tag = soup.find('div', class_="cat-series")
      if title_tag:
        title = title_tag.text.strip()
        title = re.sub(r'[\\/*?:"<>|]', "", title)
      else:
         title = 'No title found'

      content = box.text.strip()

      # Constroi o caminho e salva o conteúdo do arquivo
      file_path = os.path.join(output_dir, f'{title}.txt')

      with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
      
      print(f'title: {title}\n')
      print(f'content: {content}\n')
      print(f'Conteúdo salvo em: {file_path}')
    else:
      print(f"Elemento 'box' não encontrado no {title}.")
      break
  
  else:
        print(f"Erro ao acessar a página: Status code {site.status_code}.")

  next_url = nextpage(soup)

  if next_url:
    if not next_url.startswith('http'):
      next_url = f'https://centralnovel.com{next_url}'
    url = next_url
  else:
    break
  




