import numpy as np
from pathlib import Path
from math import tan, radians
import Objetos
from PIL import Image

# Função: transformar input em lista


def transformar_em_lista(string):
    vetor = string.split(' ')
    for g in range(3):
        vetor[g] = int(vetor[g])
    return vetor


def calcular_inicial(h, v, mv, ml, oa):
    at = oa
    if h % 2 == 0:
        at -= (ml / 2) - (ml * ((h / 2) - 1))
    else:
        at -= ml * ((h - 1) / 2)
    if v % 2 == 0:
        at -= (mv / 2) - (mv * ((v / 2) - 1))
    else:
        at -= mv * ((v - 1) / 2)
    return at


# registrando todos os objetos
obj = Objetos.Objetos()
path = Path('input.txt')
contents = path.read_text()
lines = contents.splitlines()
for line in lines:
    obj.register(line)


def phong(mtrl, luzambiente,  normal, ponto):
    # kd = 3 ks = 4 ka = 5 kr = 6 kt = 7 p = 8
    a = mtrl[8]
    od = np.array([mtrl[0], mtrl[1], mtrl[2]])
    od = np.linalg.norm(od)
    listaluzes = obj.luzes
    cor = mtrl[5] * luzambiente
    for l in listaluzes:
        vetor_luz = l[0] - ponto
        vetor_luz = vetor_luz / np.linalg.norm(vetor_luz)
        cor += l[1] * od * mtrl[3] * np.cross(normal, vetor_luz) #+ mtrl[4] *  l.intensidade * np.cross(normal, vetor_luz)
    return cor


camera = obj.return_camera()
observador = camera[5]
ponto_alvo = camera[6]
up = camera[4]
distancia_camera_tela = camera[3]
hres = int(camera[1])
vres = int(camera[2])
oa = ponto_alvo - observador
grid = np.zeros((vres, hres, 3), dtype=np.uint8)

deslocamento_lateral = np.cross(up, oa) / (np.linalg.norm(np.cross(up, oa)))
deslocamento_vertical = up / np.linalg.norm(up)

# Determinar vetor inicial
atual = calcular_inicial(hres, vres, deslocamento_vertical, deslocamento_lateral, oa)
# Varredura
k = 0
for i in range(vres):
    if i > 0:
        atual += deslocamento_vertical
        inter, t, p, mtrl, n = obj.intersect(atual, observador)
        if inter is True:
            grid[i, k] = [255, 0, 0]
            # phong(mtrl, obj.ambiente, n, p)
        else:
            grid[i, k] = [0, 0, 0]
    for k in range(hres):
        if i % 2 == 0 or i == 0:
            atual += deslocamento_lateral
            inter, t, p, mtrl, n = obj.intersect(atual, observador)
            if inter is True:
                grid[i, k] = [255, 0, 0]
                    # phong(mtrl, obj.ambiente, n, p)
            else:
                grid[i, k] = [0, 0, 0]
        else:
            atual -= deslocamento_lateral
            inter, t, p, mtrl, n = obj.intersect(atual, observador)
            if inter is True:
                grid[i, k] = [255, 0, 0]
                # phong(mtrl, obj.ambiente, n, p)
            else:
                grid[i, k] = [0, 0, 0]

imagem = Image.fromarray(grid)
imagem.show()
