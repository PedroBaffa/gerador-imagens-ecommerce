# -*- coding: utf-8 -*-
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import os
import io

# --- CONFIGURAÇÕES PRINCIPAIS ---
PASTA_FOTOS_ORIGINAIS = "fotos_originais"
PASTA_TEMPLATES = "templates"
PASTA_FONTES = "fontes"
PASTA_SAIDA = "output"
ARQUIVO_PLANILHA = "dados_baterias.csv"

# --- FUNÇÃO AJUDANTE PARA DESENHAR TEXTO ---
def desenhar_texto_com_fundo(draw, posicao_inicial, texto, fonte, cor_texto, cor_fundo, padding=15, radius=20):
    """
    Desenha um retângulo de fundo arredondado e o texto por cima.
    Retorna a posição Y final para o próximo texto.
    """
    caixa_texto = draw.textbbox(posicao_inicial, texto, font=fonte)
    pos_retangulo = (
        posicao_inicial[0] - padding,
        posicao_inicial[1] - padding,
        caixa_texto[2] + padding,
        caixa_texto[3] + padding
    )
    draw.rounded_rectangle(pos_retangulo, radius=radius, fill=cor_fundo)
    draw.text(posicao_inicial, texto, fill=cor_texto, font=fonte)
    return pos_retangulo[3] 

# --- FUNÇÃO ATUALIZADA PARA APLICAR MARCA D'ÁGUA COM AJUSTE DE POSIÇÃO ---
def aplicar_marca_dagua_diagonal(imagem_base, texto_marca, caminho_fonte, cor_fill, ajuste_x=0):
    """
    Aplica uma marca d'água de texto na diagonal sobre a imagem base,
    com um ajuste de posição horizontal opcional.
    """
    txt_layer = Image.new("RGBA", (imagem_base.width * 2, imagem_base.height * 2), (255, 255, 255, 0))
    draw_txt = ImageDraw.Draw(txt_layer)

    fonte_marca_dagua = ImageFont.truetype(caminho_fonte, 250)
    
    draw_txt.text((txt_layer.width / 2, txt_layer.height / 2), texto_marca, font=fonte_marca_dagua, fill=cor_fill, anchor="ms")

    angulo_rotacao = 40
    rotated_txt_layer = txt_layer.rotate(angulo_rotacao, expand=True)

    marca_dagua_final = Image.new("RGBA", imagem_base.size, (255, 255, 255, 0))
    
    # Adiciona o ajuste_x à posição final
    pos_x = ((marca_dagua_final.width - rotated_txt_layer.width) // 2) + ajuste_x
    pos_y = (marca_dagua_final.height - rotated_txt_layer.height) // 2
    
    marca_dagua_final.paste(rotated_txt_layer, (pos_x, pos_y), rotated_txt_layer)

    imagem_final = Image.alpha_composite(imagem_base, marca_dagua_final)
    
    return imagem_final

# --- FUNÇÃO DA CONTA 1 (HOBINHOOD) COM MARCA D'ÁGUA DESLOCADA ---
def criar_imagem_conta1(info_bateria, foto_sem_fundo):
    """
    Cria a imagem final para a HOBINHOOD com a marca d'água deslocada para a direita.
    """
    template = Image.open(os.path.join(PASTA_TEMPLATES, "template_conta1.png")).convert("RGBA")
    
    tamanho_foto = (580, 720) 
    posicao_foto = (650, 310) 
    foto_bateria_redimensionada = foto_sem_fundo.resize(tamanho_foto)
    template.paste(foto_bateria_redimensionada, posicao_foto, foto_bateria_redimensionada)

    draw = ImageDraw.Draw(template)
    caminho_fonte = os.path.join(PASTA_FONTES, "Poppins-Bold.ttf")
    
    fonte_texto = ImageFont.truetype(caminho_fonte, 42)
    cor_texto_card = (0, 0, 0, 250)
    cor_fundo_card = (255, 255, 0, 200)
    posicao_x_inicial = 65 
    posicao_y_atual = 335 
    espacamento_entre_cards = 55

    textos = [
        f"Modelo: {info_bateria['modelo']}", f"Compatível: {info_bateria['compatibilidade']}",
        f"Capacidade: {info_bateria['capacidade']}", "Qualidade: Premium",
        "90 Dias de Garantia", "Verifique a Descrição"
    ]

    for texto in textos:
        posicao_y_atual = desenhar_texto_com_fundo(
            draw, (posicao_x_inicial, posicao_y_atual), texto, fonte_texto,
            cor_texto_card, cor_fundo_card, radius=20
        ) + espacamento_entre_cards

    # Aplica a marca d'água com a SUA cor/opacidade e o ajuste de posição
    imagem_final = aplicar_marca_dagua_diagonal(
        imagem_base=template,
        texto_marca="HOBINHOOD",
        caminho_fonte=caminho_fonte,
        cor_fill=(255, 255, 255, 150), # Sua configuração de cor/opacidade restaurada
        ajuste_x=50  # <-- Ajuste de posição apenas para esta imagem
    )

    return imagem_final

# --- FUNÇÃO DA CONTA 2 (SALVATORI) SEM ALTERAÇÃO ---
def criar_imagem_conta2(info_bateria, foto_sem_fundo):
    """ Template 2 (SALVATORI) com marca d'água centralizada """
    template = Image.open(os.path.join(PASTA_TEMPLATES, "template_conta2.png")).convert("RGBA")

    tamanho_foto = (580, 720); 
    posicao_foto = (650, 310)
    foto_bateria_redimensionada = foto_sem_fundo.resize(tamanho_foto)
    template.paste(foto_bateria_redimensionada, posicao_foto, foto_bateria_redimensionada)
    
    draw = ImageDraw.Draw(template)

    caminho_fonte = os.path.join(PASTA_FONTES, "Poppins-Bold.ttf")
    fonte_texto = ImageFont.truetype(caminho_fonte, 42)
    cor_texto_card = (255, 255, 255)
    cor_fundo_card = (200, 0, 0, 220)
    posicao_x_inicial = 65
    posicao_y_atual = 335
    espacamento_entre_cards = 55

    textos = [
        f"Modelo: {info_bateria['modelo']}", f"Compatível: {info_bateria['compatibilidade']}",
        f"Capacidade: {info_bateria['capacidade']}", "Qualidade: Premium",
        "90 Dias de Garantia", "Verifique a Descrição"
    ]

    for texto in textos:
        posicao_y_atual = desenhar_texto_com_fundo(
            draw, (posicao_x_inicial, posicao_y_atual), texto, fonte_texto,
            cor_texto_card, cor_fundo_card, radius=20
        ) + espacamento_entre_cards

    # Aplica a marca d'água com a SUA cor/opacidade e centralizada
    imagem_final = aplicar_marca_dagua_diagonal(
        imagem_base=template,
        texto_marca="SALVATORI",
        caminho_fonte=caminho_fonte,
        cor_fill=(143, 143, 143, 180) # Sua configuração de cor/opacidade restaurada
    )
    
    return imagem_final

# --- FUNÇÃO DA CONTA 3 (CLARA CELL) SEM ALTERAÇÃO ---
def criar_imagem_conta3(info_bateria, foto_sem_fundo):
    """ Template 3 (CLARA CELL) com marca d'água centralizada """
    template = Image.open(os.path.join(PASTA_TEMPLATES, "template_conta3.png")).convert("RGBA")

    tamanho_foto = (580, 720); 
    posicao_foto = (650, 310)
    foto_bateria_redimensionada = foto_sem_fundo.resize(tamanho_foto)
    template.paste(foto_bateria_redimensionada, posicao_foto, foto_bateria_redimensionada)

    draw = ImageDraw.Draw(template)

    caminho_fonte = os.path.join(PASTA_FONTES, "Poppins-Bold.ttf")
    fonte_texto = ImageFont.truetype(caminho_fonte, 42)
    cor_texto_card = (255, 255, 255)
    cor_fundo_card = (0, 0, 255, 220)
    posicao_x_inicial = 65
    posicao_y_atual = 335
    espacamento_entre_cards = 55

    textos = [
        f"Modelo: {info_bateria['modelo']}", f"Compatível: {info_bateria['compatibilidade']}",
        f"Capacidade: {info_bateria['capacidade']}", "Qualidade: Premium",
        "90 Dias de Garantia", "Verifique a Descrição"
    ]
    
    for texto in textos:
        posicao_y_atual = desenhar_texto_com_fundo(
            draw, (posicao_x_inicial, posicao_y_atual), texto, fonte_texto,
            cor_texto_card, cor_fundo_card, radius=35
        ) + espacamento_entre_cards

    # Aplica a marca d'água com a SUA cor/opacidade e centralizada
    imagem_final = aplicar_marca_dagua_diagonal(
        imagem_base=template,
        texto_marca="CLARA CELL",
        caminho_fonte=caminho_fonte,
        cor_fill=(0, 0, 0, 180) # Sua configuração de cor/opacidade restaurada
    )
    
    return imagem_final


# --- PROGRAMA PRINCIPAL (Sem alterações) ---
def main():
    print("Verificando pastas de saída...")
    os.makedirs(os.path.join(PASTA_SAIDA, "conta1"), exist_ok=True)
    os.makedirs(os.path.join(PASTA_SAIDA, "conta2"), exist_ok=True)
    os.makedirs(os.path.join(PASTA_SAIDA, "conta3"), exist_ok=True)
    print(f"Lendo dados da planilha '{ARQUIVO_PLANILHA}'...")
    try:
        df_baterias = pd.read_csv(ARQUIVO_PLANILHA)
    except UnicodeDecodeError:
        print("Falha ao ler como UTF-8, tentando como latin-1...")
        df_baterias = pd.read_csv(ARQUIVO_PLANILHA, encoding='latin-1')
    except FileNotFoundError:
        print(f"ERRO: Planilha '{ARQUIVO_PLANILHA}' não encontrada!")
        return
    df_baterias.columns = df_baterias.columns.str.strip()
    print("Colunas encontradas na planilha:", df_baterias.columns.tolist())
    print(f"Encontradas {len(df_baterias)} baterias para processar.")
    for indice, linha in df_baterias.iterrows():
        sku = str(linha['sku'])
        modelo = str(linha['modelo'])
        arquivo_foto = str(linha['arquivo_foto'])
        caminho_foto_original = os.path.join(PASTA_FOTOS_ORIGINAIS, arquivo_foto)
        print(f"\nProcessando Bateria: SKU {sku} - Modelo {modelo}")
        if not os.path.exists(caminho_foto_original):
            print(f"AVISO: Foto '{arquivo_foto}' não encontrada. Pulando este item.")
            continue
        print("  -> Removendo o fundo da foto...")
        with open(caminho_foto_original, "rb") as f:
            foto_original_bytes = f.read()
            foto_sem_fundo_bytes = remove(foto_original_bytes)
        foto_sem_fundo = Image.open(io.BytesIO(foto_sem_fundo_bytes))
        nome_arquivo_saida = f"{sku}-{modelo}.png"
        print("  -> Gerando imagem para a Conta 1 (HOBINHOOD)...")
        img1 = criar_imagem_conta1(linha, foto_sem_fundo)
        img1.save(os.path.join(PASTA_SAIDA, "conta1", nome_arquivo_saida))
        print("  -> Gerando imagem para a Conta 2 (SALVATORI)...")
        img2 = criar_imagem_conta2(linha, foto_sem_fundo)
        img2.save(os.path.join(PASTA_SAIDA, "conta2", nome_arquivo_saida))
        print("  -> Gerando imagem para a Conta 3 (CLARA CELL)...")
        img3 = criar_imagem_conta3(linha, foto_sem_fundo)
        img3.save(os.path.join(PASTA_SAIDA, "conta3", nome_arquivo_saida))
    print("\nProcesso concluído com sucesso! Verifique a pasta 'output'.")

if __name__ == "__main__":
    main()