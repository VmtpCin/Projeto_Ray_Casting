# Definindo objetos e interseções com retas
import numpy as np
from numpy.linalg import norm
from math import sqrt, inf, sin, cos, acos, floor
from Interseções import *
import cv2 as cv

lista_faces = []
lista_pontos = []

def criar_triangulo(v1, v2, v3, numero_vertices, lista_faces):
    lista_faces.append([np.array(v1), np.array(v2), np.array(v3), numero_vertices])


def criar_malha(lista_faces):
    num_vertices = int(input())
    num_faces = int(input())
    lista_vertices = []
    for i in range(num_vertices):
        vertice = np.array(input().split(), dtype='float')
        lista_vertices.append(vertice)
    for i in range(num_faces):
        numero_vertices = np.array(input().split(), dtype='int')
        v1 = lista_vertices[numero_vertices[0]]
        v2 = lista_vertices[numero_vertices[1]]
        v3 = lista_vertices[numero_vertices[2]]
        criar_triangulo(v1, v2, v3, numero_vertices, lista_faces)

def read_stl(path, lista_faces):
    lista_vertices = []
    lista_vertices_str = []
    with open(path, 'r') as file:
        lines = file.readlines()
        count = 0
        numero_vertices = []
        tri = []
        for line in lines:
            parts = line.split()
            if len(parts) == 4 and parts[0] == 'vertex':
                count += 1
                vertice = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
                vertice_str = parts[1] + ' ' + parts[2] + ' ' + parts[3]
                if vertice_str not in lista_vertices_str:
                    lista_vertices.append(vertice)
                    lista_vertices_str.append(vertice_str)
                    numero_vertices.append(lista_vertices_str.index(vertice_str))
                else:
                    numero_vertices.append(lista_vertices_str.index(vertice_str))
                tri.append(vertice)

                if count == 3:
                    count = 0
                    criar_triangulo(tri[0], tri[1], tri[2], numero_vertices, lista_faces)
                    tri = []
                    numero_vertices = []


def read_obj(path, lista_faces):
    lista_vertices = []
    with open(path, 'r') as file:
        lines = file.readlines()
        numero_vertices = []
        for line in lines:
            parts = line.split()
            if len(parts) > 0:
                if parts[0] == 'v':
                    vertice = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
                    lista_vertices.append(vertice)

                elif parts[0] == 'f':
                    for str in parts[1:]:
                        index = int(str.split('/')[0]) - 1
                        numero_vertices.append(index)
                    v1 = lista_vertices[numero_vertices[0]]
                    v2 = lista_vertices[numero_vertices[1]]
                    v3 = lista_vertices[numero_vertices[2]]
                    criar_triangulo(v1, v2, v3, numero_vertices, lista_faces)
                    numero_vertices = []



def gerar_aresta(v1, v2, diametro):
    vetor_da_aresta = v1 - v2
    modulo_da_aresta = np.linalg.norm(vetor_da_aresta)
    num_particulas = floor(modulo_da_aresta / diametro)
    offset = vetor_da_aresta / num_particulas
    for i in range(num_particulas + 1):
        lista_pontos.append(v2 + (i * offset))

def normalize(v):
    norma = norm(v)
    if norma == 0:
        return v
    return v / norma

def gerar_interior(tri, diametro):
    aresta1 = tri[1] - tri[0]
    aresta2 = tri[0] - tri[2]
    aresta3 = tri[2] - tri[1]
    arestas = [aresta1, aresta2, aresta3]

    temp = 0
    maior_aresta = np.array([0, 0, 0])
    temp1 = 100000
    menor_aresta = np.array([0, 0, 0])
    atual = 0

    for a in arestas:
        if np.linalg.norm(a) > temp:
            temp = np.linalg.norm(a)
            maior_aresta = a
        elif np.linalg.norm(a) < temp1:
            temp1 = np.linalg.norm(a)
            menor_aresta = a

    if np.array_equal(menor_aresta, aresta1):
        v1 = tri[0]
        v2 = tri[1]
        v3 = tri[2]
        atual = 1
    if np.array_equal(menor_aresta, aresta2):
        v1 = tri[0]
        v2 = tri[2]
        v3 = tri[1]
        atual = 2
    if np.array_equal(menor_aresta, aresta3):
        v1 = tri[1]
        v2 = tri[2]
        v3 = tri[0]
        atual = 3


    normal_interna_da_menor = normalize(np.cross(menor_aresta, np.cross(maior_aresta, menor_aresta)))


    ht = abs(np.dot(normal_interna_da_menor, maior_aresta))
    num_passos = floor(ht / diametro)

    for i in range(num_passos):
        scanline_vetor = menor_aresta
        count = ht * ((i+1)/num_passos)
        ponto_scanline = v1 + count * normal_interna_da_menor
        a = scanline_vetor
        b1 = v3 - v1
        b2 = v3 - v2
        c = ponto_scanline - v3

        t1 = (np.dot(np.cross(c, b1), np.cross(a, b1)) / np.linalg.norm(np.cross(a, b1)**2)) * -1
        t2 = (np.dot(np.cross(c, b2), np.cross(a, b2)) / np.linalg.norm(np.cross(a, b2)**2)) * -1

        vs1 = ponto_scanline + t1 * scanline_vetor
        vs2 = ponto_scanline + t2 * scanline_vetor

        gerar_aresta(vs1, vs2, diametro)





def gerar_pontos(lista_faces):
    diametro_particula = 0.1
    lista_arestas_formadas = []
    for tri in lista_faces:
        ndv = tri[3] #num dos vertices
        if (ndv[0], ndv[1]) not in lista_arestas_formadas:
            gerar_aresta(tri[0], tri[1], diametro_particula)
            lista_arestas_formadas.append((ndv[0], ndv[1]))
            lista_arestas_formadas.append((ndv[1], ndv[0]))
        if (ndv[0], ndv[2]) not in lista_arestas_formadas:
            gerar_aresta(tri[0], tri[2], diametro_particula)
            lista_arestas_formadas.append((ndv[0], ndv[2]))
            lista_arestas_formadas.append((ndv[2], ndv[0]))
        if (ndv[1], ndv[2]) not in lista_arestas_formadas:
            gerar_aresta(tri[1], tri[2], diametro_particula)
            lista_arestas_formadas.append((ndv[1], ndv[2]))
            lista_arestas_formadas.append((ndv[2], ndv[1]))

        #gerar_interior(tri, diametro_particula)


def vetor_deslocamento(x, y, k, m, b, u):
    dl = ((2 * x) / (k - 1)) * b
    dv = ((2 * y) / (m - 1)) * u
    return dl, dv

def raycast(lista_objetos):
    camera = np.array([-50, 0, -5])
    alvo = np.array([1, 0, 1])
    vetor_up = np.array([0, 1, 0])

    distancia = 1
    hres = 500
    vres = 500
    tamx = 0.5
    tamy = 0.5

    grid = np.zeros((vres, hres, 3), dtype=np.uint8)

    oa = normalize(alvo - camera)
    b = normalize(np.cross(vetor_up, oa))
    up = normalize(-1 * np.cross(oa, b))

    desl_l, desl_v = vetor_deslocamento(tamx, tamy, hres, vres, b, up)
    vet_incial = oa * distancia - tamx * b - tamy * up

    vet_at = vet_incial
    for i in range(vres):
        if i > 0:
            vet_at[2] = vet_incial[2]
            vet_at = vet_at + desl_v
        for k in range(hres):
            if k > 0:
                vet_at = vet_at + desl_l
            grid[i, k] = intersecao_rt(camera, vet_at, distancia, inf, lista_objetos)

    cv.imshow('i', grid)
    cv.waitKey(0)
    cv.destroyWindow('i')

def starfield_projection(photons):
    camera = np.array([-40, 0, 1])
    alvo = np.array([1, 0, -1])
    vetor_up = np.array([0, 1, 0])

    distancia = 1
    hres = 500
    vres = 500
    tamx = 0.5
    tamy = 0.5

    grid = np.zeros((vres, hres, 3), dtype=np.uint8)

    oa = normalize(alvo - camera)
    b = normalize(np.cross(vetor_up, oa))
    up = normalize(-1 * np.cross(oa, b))

    desl_l, desl_v = vetor_deslocamento(tamx, tamy, hres, vres, b, up)
    vet_incial = oa * distancia - tamx * b - tamy * up

    intersecta_i, t_i, p_i, n, rr, ir = intersecao_pl(["pl", np.array(oa) * distancia + camera, np.array(camera - alvo), [0, 0, 0], 0], camera, vet_incial)

    cnt = 0
    for photon in photons:


        vetor_proj = camera - photon
        testar_direcao = np.dot(vetor_proj, oa)
        tipo = photon[1]

        intersecta, t, p, n, rr, ir = intersecao_pl(["pl",  np.array(oa) * distancia + camera, np.array(camera - alvo), [0, 0, 0], 0], photon, vetor_proj)

        if intersecta is True and testar_direcao < 0:

            vetor = p - p_i

            v_desl_l = np.divide(vetor, desl_l, out=np.zeros_like(vetor), where=desl_l != 0)

            if min(v_desl_l) == 0:
                num_des_l = max(v_desl_l)
            else:
                num_des_l = min(v_desl_l)

            v_desl_v = np.divide(vetor, desl_v, out=np.zeros_like(vetor), where=desl_v != 0)

            if min(v_desl_v) == 0:
                num_des_v = max(v_desl_v)
            else:
                num_des_v = min(v_desl_v)

            posicao_grid_y = round(num_des_l)
            posicao_grid_x = round(num_des_v)

            # print(posicao_grid_x, posicao_grid_y)

            if 0 <= posicao_grid_x <= hres - 1 and 0 <= posicao_grid_y <= vres - 1:
                grid[posicao_grid_x, posicao_grid_y] = [255, 255, 255]

    cv.imshow('i', grid)
    cv.waitKey(0)
    cv.destroyWindow('i')




#criar_malha(lista_faces)
read_stl('cube.stl', lista_faces)
#read_obj('cube.obj', lista_faces)
gerar_pontos(lista_faces)
starfield_projection(lista_pontos)
raycast(lista_faces)
