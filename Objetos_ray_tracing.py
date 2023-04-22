import numpy as np
import sympy
from math import sqrt

# Mtrl = [or, og, ob, kd, ks, ka, kr, kt, p]


def transformar_em_lista(string):
    vetor = string.split(' ')
    for g in range(len(vetor)):
        vetor[g] = float(vetor[g])
    return vetor


def registrar_camera():
    ponto_observador = np.array(transformar_em_lista(input('')))
    ponto_alvo = np.array(transformar_em_lista(input('')))
    vetor_up_w = np.array(transformar_em_lista(input('')))
    angulo_de_visao = 90  # int(input(''))
    distancia_obs_tela = 1  # int(input(''))
    pixels_largura_k = 500  # int(input(''))
    pixels_altura_m = 500  # int(input(''))
    camera = [ponto_observador, ponto_alvo, vetor_up_w, angulo_de_visao, distancia_obs_tela, pixels_largura_k, pixels_altura_m]
    return camera


def registrar_objetos():
    objetos = {}
    num_de_objetos = int(input(''))
    for i in range(num_de_objetos):
        tipo = input('')
        if tipo == '1':
            raio = int(input(''))
            centro = np.array(transformar_em_lista(input('')))
            mtrl = np.array(transformar_em_lista(input('')))
            objeto = ['Esfera', raio, centro, mtrl]
            objetos[i] = objeto
        elif tipo == '2':
            vetor_normal_plano = np.array(transformar_em_lista(input('')))
            ponto = np.array(transformar_em_lista(input('')))
            mtrl = np.array(transformar_em_lista(input('')))
            objeto = ['Plano', vetor_normal_plano, ponto, mtrl]
            objetos[i] = objeto
        elif tipo == "3":
            lista_vertices = []
            lista_triangulos = []
            lista_normal_faces = []
            lista_normal_vertices = []
            num_triangulos = int(input(''))
            num_vertices = int(input(''))
            for v in range(num_vertices):
                vertice = np.array(transformar_em_lista(input('')))
                lista_vertices.append(vertice)
            for t in range(num_triangulos):
                triangulo = transformar_em_lista(input(''))
                lista_triangulos.append(triangulo)
            for j in range(num_triangulos):
                ponto1 = lista_vertices[lista_triangulos[j][0]]
                ponto2 = lista_vertices[lista_triangulos[j][1]]
                ponto3 = lista_vertices[lista_triangulos[j][2]]
                normal = np.cross((ponto1 - ponto2), (ponto1 - ponto3))
                lista_normal_faces.append(normal)
            for v in range(num_vertices):
                cont = 0
                soma_normais_faces_adjacentes = 0
                for k in range(num_triangulos):
                    if v in lista_triangulos[k]:
                        soma_normais_faces_adjacentes += lista_normal_faces[k]
                        cont += 1
                normal_vertice = soma_normais_faces_adjacentes/cont
                lista_normal_vertices.append(normal_vertice)
            for t in range(num_triangulos):
                ponto1 = lista_vertices[lista_triangulos[t][0]]
                ponto2 = lista_vertices[lista_triangulos[t][1]]
                ponto3 = lista_vertices[lista_triangulos[t][2]]
                normal = np.cross((ponto1 - ponto2), (ponto1 - ponto3))
                objeto = ['triangulo', ponto1, ponto2, ponto3, normal,  lista_triangulos[t], lista_normal_vertices]
                objetos[t] = objeto
    return objetos


def registrar_luzes():
    ambiente = float(input(''))
    luzes = []
    num_luzes = int(input(''))
    for i in range(num_luzes):
        local = np.array(transformar_em_lista(input('')))
        intensidade = float(input(''))
        luz = [local, intensidade]
        luzes.append(luz)
    return luzes, ambiente


def intersecao(obj, vet, obs):
    men_t = 999999999999
    primeira_interseccao = -1
    tipo = 0
    ponto = [0, 0, 0]
    ponto_temp = []
    normal = [0, 0, 0]
    normal_temp = []
    mtrl = [0, 0, 0]
    keys = obj.keys()
    for i in range(len(keys)):
        if obj[i][0] == 'Esfera':
            inter, t, ponto_temp, normal_temp, mtrl = intersecao_esfera(obj[i], vet, obs)
            if inter is True and t < men_t:
                men_t = t
                primeira_interseccao = i
                normal = normal_temp
                ponto = ponto_temp
                tipo = 1
        elif obj[i][0] == 'Plano':
            inter, t, ponto_temp, normal_temp, mtrl = intersecao_plano(obj[i], vet, obs)
            if inter is True and t < men_t:
                men_t = t
                primeira_interseccao = i
                normal = normal_temp
                ponto = ponto_temp
                tipo = 2
        elif obj[i][0] == 'triangulo':
            inter, t, ponto_temp, normal_temp, mtrl = intersecao_triangulo(obj[i], vet, obs)
            if inter is True and t < men_t:
                men_t = t
                primeira_interseccao = i
                normal = normal_temp
                ponto = ponto_temp
                tipo = 3
    return primeira_interseccao, ponto, normal, mtrl, tipo


def intersecao_esfera(esf, vet, obs):
    a = np.linalg.norm(vet)**2
    b = 2 * (np.dot(vet, obs) - np.dot(vet, esf[2]))
    c = np.linalg.norm(obs) - (2 * np.dot(esf[2], obs)) + np.linalg.norm(esf[2])**2 - esf[1]**2
    delta = b**2 - (4*a*c)

    if delta < 0:
        return False, -1, 0, 0, 0

    it1 = (-b + sqrt(delta))/2*a
    it2 = (-b - sqrt(delta))/2*a

    if it1 < it2:
        menor_t = it1
    else:
        menor_t = it2

    x = obs[0] + menor_t * vet[0]
    y = obs[1] + menor_t * vet[1]
    z = obs[2] + menor_t * vet[2]
    ponto = np.array([x, y, z])
    normal = ponto - esf[2]

    if it1 < 0 and it2 < 0:
        return False, -1, 0, 0, 0
    else:
        return True, menor_t, ponto, normal, esf[3]


def intersecao_plano(pla, vet, obs):
    try:
        t = (np.dot(pla[1], pla[2]) - np.dot(pla[1], obs))/np.dot(pla[1], vet)
        x = obs[0] + t * vet[0]
        y = obs[1] + t * vet[1]
        z = obs[2] + t * vet[2]
        ponto = np.array([x, y, z])
        return True, t, ponto, pla[1], pla[3]
    except EOFError:
        return False, -1, 0, 0, 0


def intersecao_triangulo(tri, vet, obs):
    try:
        t = (np.dot(tri[4], tri[1]) - np.dot(tri[4], obs))/np.dot(tri[4], vet)
        x = obs[0] + t * vet[0]
        y = obs[1] + t * vet[1]
        z = obs[2] + t * vet[2]
        ponto = np.array([x, y, z])
        mtrl = 0
        lin1 = [tri[1][0], tri[2][0], tri[3][0]]
        lin2 = [tri[1][1], tri[2][1], tri[3][1]]
        lin3 = [tri[1][2], tri[2][2], tri[3][2]]
        matriz1 = np.array([lin1, lin2, lin3, [1, 1, 1]])
        matriz2 = []
        _, inds = sympy.Matrix(matriz1).T.rref()
        if 0 not in inds:
            matriz1 = np.array([lin2, lin3, [1, 1, 1]])
            matriz2 = np.array([[y], [z], [1]])
        elif 1 not in inds:
            matriz1 = np.array([lin1, lin3, [1, 1, 1]])
            matriz2 = np.array([[x], [z], [1]])
        elif 2 not in inds:
            matriz1 = np.array([lin1, lin2, [1, 1, 1]])
            matriz2 = np.array([[x], [y], [1]])
        elif 3 not in inds:
            matriz1 = np.array([lin1, lin2, lin3])
            matriz2 = np.array([[x], [y], [z]])
        resultado = np.linalg.solve(matriz1, matriz2)
        alfa = resultado[0]
        beta = resultado[1]
        gama = resultado[2]
        normal = 0  # alfa * (tri[6][tri[5][0]]) + beta * (tri[6][tri[5][1]]) + gama * (tri[6][tri[5][2]])  # Checar ordem dos vertices, tem que ser igual a ordem que descreve o ponto
        if 0 < alfa < 1 and 0 < beta < 1 and 0 < gama < 1:
            return True, t, ponto, normal, mtrl
        else:
            return False, -1, 0, 0, 0
    except EOFError:
        return False, -1, 0, 0, 0
