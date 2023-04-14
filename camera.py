import sys
import numpy as np
from math import tan, radians
import Objetos_ray_tracing as obj
from PIL import Image

from parser_input import ParserInput


# Função: transformar input em lista
def transformar_em_lista(string):
    vetor = string.split(' ')
    for g in range(3):
        vetor[g] = int(vetor[g])
    return vetor


# Função: Encontrar vetores de deslocamento
def vetor_deslocamento(up, oa, taml, tamv, pxl, pxv):
    versor_deslocamento_lateral = np.cross(up, oa) / (np.linalg.norm(np.cross(up, oa)))
    versor_deslocamento_vertical = up / np.linalg.norm(up)
    largura_do_pixel = taml/pxl
    altura_do_pixel = tamv/pxv
    deslocamento_lateral = versor_deslocamento_lateral * largura_do_pixel
    deslocamento_vertical = versor_deslocamento_vertical * altura_do_pixel
    return deslocamento_lateral, deslocamento_vertical

pi = ParserInput("input.txt")

ponto_observador = pi.camera.ponto_observador
ponto_alvo = pi.camera.ponto_alvo
vetor_up = pi.camera.vetor_up
angulo_de_visao = 60
distancia_objeto_tela = pi.camera.distancia
pixels_largura_k = pi.camera.largura
pixels_altura_m = pi.camera.altura

grid = np.zeros((pixels_altura_m, pixels_largura_k, 3), dtype=np.uint8)


# Registrar objetos
# lista_objetos = obj.registrar_objetos()
lista_objetos = pi.objetos

# Calcular Vetor_objeto_alvo
vetor_objeto_alvo = ponto_alvo - ponto_observador

# Determinando altura/largura da tela virtual
largura_da_tela = 2 * distancia_objeto_tela * tan(radians(angulo_de_visao))
altura_da_tela = largura_da_tela * (pixels_altura_m/pixels_largura_k)

# Criando Vetor deslocamento
vetor_deslocamento_lateral, vetor_deslocamento_vertical = vetor_deslocamento(vetor_up, vetor_objeto_alvo, largura_da_tela, altura_da_tela, pixels_largura_k, pixels_altura_m)

# Loop
# Determinando vetor inicial
vetor_centro_lateral = vetor_objeto_alvo - (vetor_deslocamento_lateral * ((pixels_largura_k - 1)/2))
vetor_inicial = vetor_centro_lateral - (vetor_deslocamento_vertical * ((pixels_altura_m - 1)/2))

# Varredura
vetor_atual = vetor_inicial
for i in range(pixels_altura_m):
    if i > 0:
        vetor_atual = vetor_atual + vetor_deslocamento_vertical - (vetor_deslocamento_lateral * (pixels_largura_k - 1))
    for k in range(pixels_largura_k):
        if k > 0:
            vetor_atual = vetor_atual + vetor_deslocamento_lateral
        print(vetor_atual)
        primeira_i = obj.intersecao(lista_objetos, vetor_atual, ponto_observador)
        if primeira_i < 0:
            grid[i, k] = [255, 255, 255]
        elif lista_objetos[primeira_i][0] == 'Esfera':
            grid[i, k] = [255, 0, 0]
        elif lista_objetos[primeira_i][0] == 'Plano':
            grid[i, k] = [0, 255, 0]

imagem = Image.fromarray(grid)
imagem.show()
