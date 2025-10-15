# Gerador de Imagens para E-commerce

Este projeto é um script em Python que automatiza a criação de imagens de produtos para diferentes lojas online, utilizando modelos pré-definidos e dados de uma folha de cálculo.

## Funcionalidades

- Lê dados de produtos de um ficheiro `.csv`.
- Remove o fundo de imagens de produtos automaticamente.
- Aplica a imagem do produto e as suas informações em múltiplos modelos.
- Adiciona uma marca d'água personalizada para cada modelo.
- Guarda as imagens finais em pastas organizadas.

## Estrutura do Projeto

- `gerar_imagens.py`: O script principal que executa toda a lógica.
- `dados_baterias.csv`: A folha de cálculo com as informações dos produtos.
- `fotos_originais/`: Pasta para as imagens originais dos produtos.
- `templates/`: Pasta para os ficheiros de imagem que servem como fundo.
- `fontes/`: Pasta para os ficheiros de fontes de texto.
- `output/`: Pasta onde as imagens geradas são guardadas (ignorada pelo Git).

## Como Usar

1.  **Clonar o repositório (opcional):**
    ```bash
    git clone https://github.com/PedroBaffa/gerador-imagens-ecommerce.git
    cd SEU-REPOSITORIO
    ```

2.  **Instalar as dependências:**
    Com o ficheiro `requirements.txt`, podes instalar todas as bibliotecas necessárias com um único comando:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Preparar os ficheiros:**
    - Adiciona as tuas fotos na pasta `fotos_originais/`.
    - Atualiza a folha de cálculo `dados_baterias.csv` com os dados dos teus produtos.
    - Personaliza as imagens na pasta `templates/` se necessário.

4.  **Executar o script:**
    ```bash
    python gerar_imagens.py
    ```

As imagens finais serão criadas na pasta `output/`.