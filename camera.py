import numpy as np
from math import tan


# Função: transformar input em lista
def transformar_em_lista(string):
    vetor = string.split(' ')
    for g in range(3):
        vetor[g] = int(vetor[g])
    return vetor


# Função: Encontrar vetores de deslocamento
def vetor_deslocamento(up, oa, taml, tamv, pxl, pxv):
    versor_desolocamento_lateral = np.cross(up, oa) / (np.linalg.norm(np.cross(up, oa)))
    versor_deslocamento_vertical = up / np.linalg.norm(up)
    largura_do_pixel = taml/(pxl - 1)
    altura_do_pixel = tamv/(pxv - 1)
    deslocamento_lateral = versor_desolocamento_lateral * largura_do_pixel
    deslocamento_vertical = versor_deslocamento_vertical * altura_do_pixel
    return deslocamento_lateral, deslocamento_vertical


ponto_observador = np.array(transformar_em_lista(input('')))
ponto_alvo = np.array(transformar_em_lista(input('')))
vetor_up = np.array(transformar_em_lista(input('')))
angulo_de_visao = int(input(''))
distancia_objeto_tela = int(input(''))
pixels_largura_k = int(input(''))
pixels_altura_m = int(input(''))

# Calcular Vetor_objeto_alvo
vetor_objeto_alvo = ponto_alvo - ponto_observador

# Determinando altura/largura da tela virtual
largura_da_tela = 2 * distancia_objeto_tela * tan(angulo_de_visao)
altura_da_tela = largura_da_tela * (pixels_altura_m/pixels_largura_k)

# Criando Vetor deslocamento
vetor_deslocamento_lateral, vetor_deslocamento_vertical = vetor_deslocamento(vetor_up, vetor_objeto_alvo, largura_da_tela, altura_da_tela, pixels_largura_k, pixels_altura_m)

# Loop
# Determinando vetor inicial
vetor_centro_lateral = vetor_objeto_alvo - (vetor_deslocamento_lateral * (largura_da_tela/2))
vetor_inicial = vetor_centro_lateral - (vetor_deslocamento_vertical * (altura_da_tela/2))

# Varredura
vetor_atual = vetor_inicial
for i in range(pixels_altura_m):
    if i > 0:
        vetor_atual = vetor_atual + vetor_deslocamento_vertical
    for k in range(pixels_largura_k):
        vetor_atual = vetor_atual + vetor_deslocamento_lateral
        print(vetor_atual)
