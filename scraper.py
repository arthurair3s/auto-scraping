import requests
from bs4 import BeautifulSoup
import re
import os

# Diretório onde os arquivos serão salvos
output_dir = 'capitulos'

# Verificar se o diretório existe, caso contrário, criar
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Definindo o volume e o capítulo inicial
volume = 1
chapter = 1

# Loop para percorrer os volumes e capítulos
while True:
    # Formatação da URL e cabeçalhos HTTP
    url = f'https://novelmania.com.br/novels/magus-supremo-ms/capitulos/volume-{volume}-capitulo-{chapter}'
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

    # Fazendo a requisição HTTP
    site = requests.get(url, headers=headers)
    
    # Verificando se a requisição foi bem-sucedida
    if site.status_code == 200:
        soup = BeautifulSoup(site.content, 'html.parser')
        box = soup.find('div', class_='text')

        # Verificando se o elemento 'box' foi encontrado
        if box:
            # Extração e limpeza do título
            title = box.find('h2', class_="mt-0 mb-3 text-center").text
            title = re.sub(r'[\\/*?:"<>|]', "", title)

            # Remoção de elementos desnecessários e extração do conteúdo
            for tag in box(['h3']):
                tag.decompose()
            content = box.text.strip()

            # Construir o caminho completo para o arquivo
            file_path = os.path.join(output_dir, f'{title}.txt')

            # Salvando o conteúdo em um arquivo
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f'Conteúdo salvo em: {file_path}')
            print(content)

            # Incrementar o capítulo
            chapter += 1
        else:
            print(f"Elemento 'box' não encontrado no capítulo {chapter} do volume {volume}.")
            break

    else:
        print(f"Erro ao acessar a página: Status code {site.status_code} para o capítulo {chapter} do volume {volume}.")
        
        # Incrementar o volume e tentar o próximo capítulo
        volume += 1
        chapter += 1