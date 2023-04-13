import numpy as np
from math import tan, radians
import Objetos_ray_tracing as obj
from PIL import Image


# Função: transformar input em lista
def transformar_em_lista(string):
    vetor = string.split(' ')
    for g in range(3):
        vetor[g] = int(vetor[g])
    return vetor


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm


# Função: Encontrar vetores de deslocamento
def vetor_deslocamento(up, b, tamx, tamy, k, m):
    deslocamento_lateral = (2*tamx/(k-1)) * b
    deslocamento_vertical = (2*tamy/(m-1)) * up
    return deslocamento_vertical, deslocamento_lateral


ponto_observador = np.array(transformar_em_lista(input('')))
ponto_alvo = np.array(transformar_em_lista(input('')))
vetor_up_w = np.array(transformar_em_lista(input('')))
angulo_de_visao = int(input(''))
distancia_obs_tela = int(input(''))
pixels_largura_k = int(input(''))
pixels_altura_m = int(input(''))
grid = np.zeros((pixels_altura_m, pixels_largura_k, 3), dtype=np.uint8)


# Registrar objetos
lista_objetos = obj.registrar_objetos()

# Calcular Vetor_objeto_alvo
vetor_objeto_alvo = ponto_alvo - ponto_observador

# Normalisando a base
oa_norm = normalize(vetor_objeto_alvo)
vetor_b = normalize(np.cross(vetor_up_w, oa_norm))
vetor_up_v = np.cross(oa_norm, vetor_b)

# Calculando tamanho da tela
tam_x = distancia_obs_tela * tan(radians(angulo_de_visao/2))
tam_y = tam_x * (pixels_altura_m/pixels_largura_k)

# Criando Vetor deslocamento
vetor_deslocamento_vertical, vetor_deslocamento_lateral = vetor_deslocamento(vetor_up_v, vetor_b, tam_x, tam_y, pixels_largura_k, pixels_altura_m)

# Loop
# Determinando vetor inicial
vetor_inicial = oa_norm * distancia_obs_tela - tam_x*vetor_b - tam_y * vetor_up_v

# Varredura
vetor_atual = vetor_inicial
for i in range(pixels_altura_m):
    if i > 0:
        vetor_atual[2] = vetor_inicial[2]
        vetor_atual = vetor_atual + vetor_deslocamento_vertical
    for k in range(pixels_largura_k):
        if k > 0:
            vetor_atual = vetor_atual + vetor_deslocamento_lateral
        print(vetor_atual)
        primeira_i = obj.intersecao(lista_objetos, vetor_atual, ponto_observador)
        if primeira_i < 0:
            grid[i, k] = [0, 0, 0]
        elif lista_objetos[primeira_i][0] == 'Esfera':
            grid[i, k] = [255, 0, 0]
        elif lista_objetos[primeira_i][0] == 'Plano':
            grid[i, k] = [0, 255, 0]

imagem = Image.fromarray(grid)
imagem.show()
