import numpy as np
from math import sqrt

# Mtrl = [or, og, ob, kd, ks, ka, kr, kt, p]


def transformar_em_lista(string):
    vetor = string.split(' ')
    for g in range(len(vetor)):
        vetor[g] = int(vetor[g])
    return vetor


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
    return objetos


def registrar_luzes():
    ambiente = np.array(transformar_em_lista(input('')))
    luzes = []
    num_luzes = int(input(''))
    for i in range(num_luzes):
        local = np.array(transformar_em_lista(input('')))
        intensidade = np.array(transformar_em_lista(input('')))
        luz = [local, intensidade]
        luzes.append(luz)
    return luzes, ambiente


def intersecao(obj, vet, obs):
    men_t = 999999999999
    primeira_interseccao = -1
    ponto = [0, 0, 0]
    normal = [0, 0, 0]
    mtrl = [0, 0, 0]
    keys = obj.keys()
    for i in range(len(keys)):
        if obj[i][0] == 'Esfera':
            inter, t, ponto, normal, mtrl = intersecao_esfera(obj[i], vet, obs)
            if inter is True and t < men_t:
                men_t = t
                primeira_interseccao = i
        elif obj[i][0] == 'Plano':
            inter, t, ponto, normal, mtrl = intersecao_plano(obj[i], vet, obs)
            if inter is True and t < men_t:
                men_t = t
                primeira_interseccao = i
    return primeira_interseccao, ponto, normal, mtrl


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
        it = (np.dot(pla[1], obs) - np.dot(pla[1], pla[2]))/np.dot(pla[1], vet)
        return True, it
    except EOFError:
        return False, -1

    # x = obs[0] + it * vet[0]
    # y = obs[1] + it * vet[1]
    # z = obs[2] + it * vet[2]
    # return np.array([x, y, z])
