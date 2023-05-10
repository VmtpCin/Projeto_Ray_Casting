import numpy as np
from PIL import Image
from math import sqrt


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def vetor_deslocamento(x, y, k, m, b, u):
    dl = ((2 * x) / (k - 1)) * b
    dv = ((2 * y) / (m - 1)) * u
    return dl, dv


def intersect(vet, og):
    a = vet[0]**2 - vet[1]**2 + vet[2]**2
    bk = (2*og[0]*vet[0]) - (2*og[1]*vet[1]) + (2*og[2]*vet[2])
    c = og[0]**2 - og[1]**2 + og[2]**2
    delta = bk ** 2 - (4 * a * c)
    if delta > 0:
        t = (-bk - sqrt(delta))/(2*a)
        x = og[0] + (t*vet[0])
        y = og[1] + (t*vet[1])
        z = og[2] + (t*vet[2])
        if y < 0 or y > 0.8:
            return [255, 255, 255]
        ponto = np.array([x, y, z])
        normal = np.array([ponto[0], 0, ponto[2]])
        vetor_luz = np.array([0, 1, 1]) - ponto
        cosseno = np.dot(normalize(normal), normalize(vetor_luz))
        cor = 0.2
        #if cosseno < 0:
            #cosseno = 1 - cosseno
        if cosseno > 0:
            cor = cor + cosseno
        if cor > 1:
            cor = 1
        return [255 * cor, 0, 0]
    else:
        return [255, 255, 255]


camera = np.array([3, 0, 0])
alvo = np.array([0, 0, 0])
vetor_up = np.array([0, 1, 0])
distancia = 1
hres = 500
vres = 500
tamx = 0.5
tamy = 0.5
grid = np.zeros((vres, hres, 3), dtype=np.uint8)

oa = normalize(alvo - camera)
b = normalize(np.cross(oa, vetor_up))
up = normalize(-1 * np.cross(b, oa))

desl_l, desl_v = vetor_deslocamento(tamx, tamy, hres, vres, b, up)
aj = oa * distancia
ajj = tamx * b
ajk = tamy * up
vet_incial = oa * distancia - tamx * b - tamy * up

vet_at = vet_incial
for i in range(vres):
    if i > 0:
        vet_at[2] = vet_incial[2]
        vet_at = vet_at + desl_v
    for k in range(hres):
        if k > 0:
            vet_at = vet_at + desl_l
        grid[i, k] = intersect(vet_at, camera)

imagem = Image.fromarray(grid)
imagem.show()
