import requests
from bs4 import BeautifulSoup
import re
import os

# Formatação da URL, cabeçalhos e requisição HTTP
url = 'https://centralnovel.com/supreme-magus-prologo-1/'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

# Função para encontrar o link da próxima página
def nextpage(soup):
    # Procura o botão para a próxima página
    pages = soup.find('a', {'rel': 'next'})
    if pages:
        prox_page = pages['href']
        return prox_page
    else:
        return None

# Loop principal para iterar através das páginas
while url:
    # Realiza a requisição HTTP
    site = requests.get(url, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if site.status_code == 200:
        soup = BeautifulSoup(site.content, 'html.parser')
        box = soup.find('div', class_='epcontent entry-content')

        # Verificação e criação do diretório onde os arquivos serão salvos
        output_dir = 'Supreme Magus'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Verifica se o elemento 'box' foi encontrado
        if box:
            # Extração e limpeza do título e remoção de elementos desnecessários do texto
            title_tag = soup.find('div', class_="cat-series")
            if title_tag:
                title = title_tag.text.strip()
                title = re.sub(r'[\\/*?:"<>|]', "", title)
            else:
                title = 'No title found'

            # Limpeza do conteúdo do box
            content = box.text.strip()

            # Constrói o caminho e salva o conteúdo do arquivo
            file_path = os.path.join(output_dir, f'{title}.txt')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            # Exibe informações sobre o progresso
            print(f'Title: {title}\n')
            print(f'Content: {content}\n')
            print(f'Conteúdo salvo em: {file_path}')
        else:
            print(f"Elemento 'box' não encontrado.")
            break
    else:
        print(f"Erro ao acessar a página: Status code {site.status_code}.")

    # Encontra a URL da próxima página
    next_url = nextpage(soup)

    # Verifica se a próxima URL foi encontrada
    if next_url:
        if not next_url.startswith('http'):
            next_url = f'https://centralnovel.com{next_url}'
        url = next_url
    else:
        break
    