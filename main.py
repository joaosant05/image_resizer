import os
from PIL import Image

def ajustar_imagem_para_folha(imagem, largura_folha=2700, altura_folha=1800, margem_largura=2400, margem_altura=1600):
    # Verifica se a imagem tem um canal alfa (transparência)
    if imagem.mode in ("RGBA", "LA") or (imagem.mode == "P" and "transparency" in imagem.info):
        # Converte para RGBA para manipular a transparência
        imagem = imagem.convert("RGBA")
    else:
        # Converte para RGB se a imagem não tiver transparência
        imagem = imagem.convert("RGB")

    largura_original, altura_original = imagem.size

    escala_largura = margem_largura / largura_original
    escala_altura = margem_altura / altura_original
    escala_final = min(escala_largura, escala_altura)
  
    nova_largura = int(largura_original * escala_final)
    nova_altura = int(altura_original * escala_final)
    imagem_redimensionada = imagem.resize((nova_largura, nova_altura), Image.LANCZOS)
    
    folha_branca = Image.new("RGBA", (largura_folha, altura_folha), (255, 255, 255, 255))
    pos_x = (largura_folha - nova_largura) // 2
    pos_y = (altura_folha - nova_altura) // 2
    folha_branca.paste(imagem_redimensionada, (pos_x, pos_y), imagem_redimensionada if imagem.mode == "RGBA" else None)
    
    return folha_branca.convert("RGB")

def processar_diretorio(diretorio_entrada, diretorio_saida):
    if not os.path.exists(diretorio_entrada):
        print("Erro: O diretório de entrada não existe.")
        return

    os.makedirs(diretorio_saida, exist_ok=True)
    print(f"Processando imagens do diretório: {diretorio_entrada}")

    for nome_arquivo in os.listdir(diretorio_entrada):
        caminho_imagem = os.path.join(diretorio_entrada, nome_arquivo)
        
        if os.path.isfile(caminho_imagem) and nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                imagem = Image.open(caminho_imagem)
                imagem_editada = ajustar_imagem_para_folha(imagem)
                caminho_saida = os.path.join(diretorio_saida, nome_arquivo)
                imagem_editada.save(caminho_saida)
                print(f"Imagem salva: {caminho_saida}")
            except Exception as e:
                print(f"Erro ao processar {nome_arquivo}: {e}")
        else:
            print(f"Arquivo ignorado (não é imagem): {nome_arquivo}")

diretorio_base = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'image_resizer')
diretorio_entrada = os.path.join(diretorio_base, 'imagens')
diretorio_saida = os.path.join(diretorio_base, 'imagens_editadas')
processar_diretorio(diretorio_entrada, diretorio_saida)
