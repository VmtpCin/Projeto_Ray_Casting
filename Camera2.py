import numpy as np
from math import tan, radians
import Objetos_ray_tracing as Obj
from PIL import Image


# Função: transformar input em lista
def transformar_em_lista(string):
    vetor = string.split(' ')
    for g in range(len(vetor)):
        vetor[g] = int(vetor[g])
    return vetor


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


# Função: Encontrar vetores de deslocamento
def vetor_deslocamento(up, b, tamx, tamy, tk, tm):
    deslocamento_lateral = (2*tamx/(tk-1)) * b
    deslocamento_vertical = (2*tamy/(tm-1)) * up
    return deslocamento_vertical, deslocamento_lateral


def traceray(p, n, mtr, amb, luzes, obs):
    cor = mtrl[5] * amb
    for luz in luzes:
        vetor_luz = luz[0] - p
        vetor_ponto_observador = obs - p
        refletido = 2 * n * np.cross(n, vetor_luz) - vetor_luz
        cor += luz[1] * (mtr[3] * np.cross(vetor_luz, n)) + (mtr[4] * (np.cross(refletido, vetor_ponto_observador) ** mtr[8]))
    return [cor[0], cor[1], cor[2]]


# Registrar objetos
camera = Obj.registrar_camera()
lista_objetos = Obj.registrar_objetos()
# lista_luzes, ambiente = Obj.registrar_luzes()

# Criar grid
grid = np.zeros((camera[6], camera[5], 3), dtype=np.uint8)

# Calcular Vetor_objeto_alvo
vetor_objeto_alvo = camera[1] - camera[0]

# Normalisando a base
oa_norm = normalize(vetor_objeto_alvo)
vetor_b = normalize(np.cross(camera[2], oa_norm))
vetor_up_v = np.cross(oa_norm, vetor_b)

# Calculando tamanho da tela
tam_x = camera[4] * tan(radians(camera[3]/2))
tam_y = tam_x * (camera[6]/camera[5])

# Criando Vetor deslocamento
vetor_deslocamento_vertical, vetor_deslocamento_lateral = vetor_deslocamento(vetor_up_v, vetor_b, tam_x, tam_y, camera[5], camera[6])

# Loop
# Determinando vetor inicial
vetor_inicial = oa_norm * camera[4] - tam_x*vetor_b - tam_y * vetor_up_v

# Varredura
vetor_atual = vetor_inicial
contador = 0
porcentagem = 0
for i in range(camera[6]):
    if i > 0:
        vetor_atual[2] = vetor_inicial[2]
        vetor_atual = vetor_atual + vetor_deslocamento_vertical
    for k in range(camera[5]):
        if k > 0:
            vetor_atual = vetor_atual + vetor_deslocamento_lateral
        contador += 1
        porcentagem_temp = round(contador/(camera[6] * camera[5]) * 100)
        if porcentagem_temp > porcentagem:
            porcentagem = porcentagem_temp
            print(porcentagem_temp)
        primeira_i, ponto, normal, mtrl, tipo = Obj.intersecao(lista_objetos, vetor_atual, camera[0])
        if primeira_i < 0:
            grid[i, k] = [255, 255, 255]
        else:
            if tipo == 3:
                grid[i, k] = [255, 0, 0]
            else:
                grid[i, k] = [0, 255, 0]
                # traceray(ponto, normal, mtrl, lista_luzes, ambiente, camera[0])

imagem = Image.fromarray(grid)
imagem.show()
