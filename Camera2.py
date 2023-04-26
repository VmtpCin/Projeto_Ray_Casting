import numpy as np
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


cont = 0
porcentagem = 0


def contador(x, y):
    global cont
    global porcentagem
    cont += 1
    porcentagem_temp = round(cont / (x * y) * 100)
    if porcentagem_temp > porcentagem:
        porcentagem = porcentagem_temp
        print(porcentagem_temp)


# Função: Encontrar vetores de deslocamento
def vetor_deslocamento(up, b, tamx, tamy, tk, tm):
    deslocamento_lateral = (2*tamx/(tk-1)) * b
    deslocamento_vertical = (2*tamy/(tm-1)) * up
    return deslocamento_vertical, deslocamento_lateral


def shade(p, n, mtr, luzes, amb, obs):
    cor = amb
    vetor_luz = []
    for luz in luzes:
        if luz[2] == 'pontual':
            vetor_luz = luz[0] - p
        if luz[2] == 'direcional':
            vetor_luz = luz[0]
        n = normalize(n)
        cosseno_nv = np.dot(n, vetor_luz)
        refletido = normalize((2 * n * cosseno_nv) - vetor_luz)
        vetor_po = normalize(obs - p)
        cosseno_rv = np.dot(refletido, vetor_po)
        if cosseno_nv > 0:
            cor += (luz[1] * mtr[3] * (cosseno_nv / (np.linalg.norm(vetor_luz) * np.linalg.norm(n)))) + \
                   (luz[1] * mtr[4] * (cosseno_rv ** mtr[8]))
        if cor > 1:
            cor = 1
        elif cor < amb:
            cor = amb
    return np.array([mtr[0] * cor, mtr[1] * cor, mtr[2] * cor])


def traceray(objs, vet, obs, lzs, amb, r, c):
    primeira_i, ponto, normal, mtrl, tipo = Obj.intersecao(objs, vet, obs)
    if primeira_i < 0 and r == c:
        return np.array([255, 255, 255])
    elif primeira_i < 0:
        return np.array([0, 0, 0])
    refletido = 2 * normal * np.dot(normal, vet) - vet
    cor = shade(ponto, normal, mtrl, lzs, amb, obs)
    if r >= 0:
        cor_r = traceray(objs, refletido, obs, lzs, amb, r-1, c)
        y = np.array([0, 0, 0])
        if not np.array_equal(y, cor_r):
            x = cor_r[0]
            cor += [cor_r[0] * mtrl[6], cor_r[1] * mtrl[6], cor_r[2] * mtrl[6]]
    return cor


# Registrar objetos
camera = Obj.registrar_camera()
lista_objetos = Obj.registrar_objetos()
lista_luzes, ambiente = Obj.registrar_luzes()

# Criar grid
grid = np.zeros((camera[6], camera[5], 3), dtype=np.uint8)

# Calcular Vetor_objeto_alvo
vetor_objeto_alvo = camera[1] - camera[0]

# Normalisando a base
oa_norm = normalize(vetor_objeto_alvo)
vetor_b = normalize(np.cross(camera[2], oa_norm))
vetor_up_v = np.cross(oa_norm, vetor_b)

# Calculando tamanho da tela
tam_x = 0.5
tam_y = 0.5

# Criando Vetor deslocamento
vetor_deslocamento_vertical, vetor_deslocamento_lateral = vetor_deslocamento(vetor_up_v, vetor_b, tam_x, tam_y,
                                                                             camera[5], camera[6])

# Loop
# Determinando vetor inicial
vetor_inicial = oa_norm * camera[4] - tam_x * vetor_b - tam_y * vetor_up_v

# Varredura
vetor_atual = vetor_inicial
for i in range(camera[6]):
    if i > 0:
        vetor_atual[2] = vetor_inicial[2]
        vetor_atual = vetor_atual + vetor_deslocamento_vertical
    for k in range(camera[5]):
        if k > 0:
            vetor_atual = vetor_atual + vetor_deslocamento_lateral
        contador(camera[6], camera[5])
        grid[i, k] = traceray(lista_objetos, vetor_atual, camera[0], lista_luzes, ambiente, 3, 3)

imagem = Image.fromarray(grid)
imagem.show()
