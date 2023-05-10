import numpy as np
import Objetos_ray_tracing as Obj
from PIL import Image
from math import inf, sqrt, asin, acos, radians, sin, cos
from tqdm.auto import tqdm
from parser_input import ParserInput


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


def matrix_tranformation(ponto, angulo):
    # rotação de angulo graus em torno to eixo y
    x = cos(radians(angulo))
    y = sin(radians(angulo))
    matriz = np.array([[x, 0, y, 0], [0, 1, 0, 0], [-y, 0, x, 0], [0, 0, 0, 1]])
    ponto = np.array([ponto[0], ponto[1], ponto[2], 0])
    resultado = np.matmul(matriz, ponto)
    ponto = np.array([resultado[0], resultado[1], resultado[2]])
    return ponto


# Função: Encontrar vetores de deslocamento
def vetor_deslocamento(up, b, tamx, tamy, tk, tm):
    deslocamento_lateral = (2*tamx/(tk-1)) * b
    deslocamento_vertical = (2*tamy/(tm-1)) * up
    return deslocamento_vertical, deslocamento_lateral


def shade(p, n, mtr, luzes, amb, obs, t, objs):
    sdw = False
    cor = amb
    vetor_luz = []
    for luz in luzes:
        if luz[2] == 'pontual':
            vetor_luz = luz[0] - p
            sdw = shadow(p, vetor_luz, objs)
        if luz[2] == 'direcional':
            vetor_luz = luz[0]
            sdw = shadow(p, vetor_luz, objs)
        if sdw is False:
            n = normalize(n)
            vetor_luz = vetor_luz
            cosseno_nv = np.dot(n, normalize(vetor_luz))
            refletido = normalize((2 * n * cosseno_nv) - vetor_luz)
            vetor_po = normalize(obs - p)
            cosseno_rv = np.dot(refletido, vetor_po)
            if cosseno_nv > 0:
                cor += (luz[1] * mtr[3] * cosseno_nv) + (luz[1] * mtr[4] * (cosseno_rv ** mtr[8]))
            if cor > 1:
                cor = 1
    red = mtr[0] * cor
    if red > 255:
        red = 255
    green = mtr[1] * cor
    if green > 255:
        green = 255
    blue = mtr[2] * cor
    if blue > 255:
        blue = 255

    return np.array([red, green, blue])


def shadow(p, vet, objs):
    temp = 0.001
    primeira_i, ponto, normal, mtrl, tipo, t = Obj.intersecao(objs, vet, p, 0.001, 1)
    if primeira_i < 0:
        return False
    else:
        if temp < t < 1:
            return True
    return False


def refract(ir1, ir2, vet,  normal, in_out):
    n = ir1/ir2
    normal = normalize(normal)
    if in_out == 1:
        normal = -1 * normal
    cos_externo = np.dot(normal, normalize(vet))
    sen_externo = sqrt(1 - (cos_externo ** 2))
    temp = sen_externo / n
    if temp > 1:
        temp = 1
    angulo_refracao = asin(temp)
    sen_interno = sqrt(1 - (sen_externo**2))
    cos_interno = cos(angulo_refracao)
    cos_externo *= -1
    t = ((1/n) * vet) - ((cos_interno - ((1/n) * cos_externo)) * normal)
    return t


def traceray(objs, vet, obs, lzs, amb, r, min, max, in_out):
    primeira_i, ponto, normal, mtrl, tipo, t = Obj.intersecao(objs, vet, obs, min, max)
    if primeira_i < 0:
        return np.array([0, 0, 0])
    cor = shade(ponto, normal, mtrl, lzs, amb, obs, t, objs)
    cor_r = 0
    # Recursão
    if r > 0:
        if mtrl[6] > 0:
            refletido = 2 * normal * np.dot(normal, -1 * vet) - (-1 * vet)
            cor_r = traceray(objs, refletido, ponto, lzs, amb, r - 1, 0.001, inf, in_out)
        if in_out == 0:
            ir1 = 1
            ir2 = mtrl[9]
            in_out = 1
        else:
            ir1 = mtrl[9]
            ir2 = 1
            in_out = 0
        if mtrl[7] > 0:
            refratado = refract(ir1, ir2, vet,  normal, in_out)
            cor_t = traceray(objs, refratado, ponto, lzs, amb, r - 1, 0.001, inf, in_out)
            cor = cor + np.array([cor_t[0] * mtrl[7], cor_t[1] * mtrl[7], cor_t[2] * mtrl[7]])
    return cor * (1 - mtrl[6]) + (cor_r * mtrl[6])


# Registrar objetos
# camera = Obj.registrar_camera()
# lista_objetos = Obj.registrar_objetos()
# lista_luzes, ambiente = Obj.registrar_luzes()

# Resgistrando a partir de arquivo
parser = ParserInput("input.txt")
camera = parser.camera
lista_objetos = parser.objetos
lista_luzes = parser.luzes
ambiente = parser.ambiente

#camera[0] = matrix_tranformation(camera[0], 30)
#camera[1] = matrix_tranformation(camera[1], 30)

# Criar grid
grid = np.zeros((camera[5], camera[4], 3), dtype=np.uint8)

# Calcular Vetor_objeto_alvo
vetor_objeto_alvo = camera[1] - camera[0]

# Normalisando a base
oa_norm = normalize(vetor_objeto_alvo)
vetor_b = normalize(np.cross(oa_norm, camera[2]))
vetor_up_v = normalize(-1 * np.cross(vetor_b, oa_norm))

# Calculando tamanho da tela
tam_x = camera[4]/1000
tam_y = camera[5]/1000

# Criando Vetor deslocamento
vetor_deslocamento_vertical, vetor_deslocamento_lateral = vetor_deslocamento(vetor_up_v, vetor_b, tam_x, tam_y,
                                                                             camera[4], camera[5])

# Loop
# Determinando vetor inicial
vetor_inicial = oa_norm * camera[3] - tam_x * vetor_b - tam_y * vetor_up_v

# Varredura
vetor_atual = vetor_inicial
for i in tqdm(range(camera[5]), desc="Renderizando"):
    if i > 0:
        vetor_atual[2] = vetor_inicial[2]
        vetor_atual = vetor_atual + vetor_deslocamento_vertical
    for k in range(camera[4]):
        if k > 0:
            vetor_atual = vetor_atual + vetor_deslocamento_lateral
        grid[i, k] = traceray(lista_objetos, vetor_atual, camera[0], lista_luzes, ambiente, 3, 1, inf, 1)

imagem = Image.fromarray(grid)
imagem.show()
