import numpy as np
from math import sqrt


def transformar_em_lista(string):
    vetor = string.split(' ')
    for g in range(3):
        vetor[g] = int(vetor[g])
    return vetor


def registrar_objetos():
    objetos = {}
    objeto = []
    num_de_objetos = int(input(''))
    for i in range(num_de_objetos):
        tipo = input('')
        if tipo == '1':
            raio = int(input(''))
            centro = np.array(transformar_em_lista(input('')))
            objeto = ['Esfera', raio, centro]
            objetos[i] = objeto
        elif tipo == '2':
            vetor_normal_plano = input('')
            ponto = input('')
            objeto = ['Plano', vetor_normal_plano, ponto]
            objetos[i] = objeto
    return objetos


def intersecao(obj, vet, obs):
    men_t = 999999999999
    primeira_interseccao = -1
    keys = obj.keys()
    for i in range(len(keys)):
        if obj[i][0] == 'Esfera':
            inter, t, normal = intersecao_esfera(obj[i], vet, obs)
            if inter is True and t < men_t:
                men_t = t
                primeira_interseccao = i
        elif obj[i][0] == 'Plano':
            inter, t, normal = intersecao_plano(obj[i], vet, obs)
            if inter is True and t < men_t:
                men_t = t
                primeira_interseccao = i
    return primeira_interseccao


def intersecao_esfera(esf, vet, obs):
    a = np.linalg.norm(vet)**2
    b = 2 * (np.dot(vet, obs) - np.dot(vet, esf[2]))
    c = np.linalg.norm(obs) - (2 * np.dot(esf[2], obs)) + np.linalg.norm(esf[2])**2 - esf[1]**2
    delta = b**2 - (4*a*c)

    if delta < 0:
        return False, -1, None

    it1 = (-b + sqrt(delta))/2*a
    it2 = (-b - sqrt(delta))/2*a

    if it1 < it2:
        menor_t = it1
    else:
        menor_t = it2

    if it1 < 0 and it2 < 0:
        return False, -1, None

    centro = esf[2]
    ponto_intersecao = np.array([obs[0] + menor_t * vet[0],
                                 obs[1] + menor_t * vet[1],
                                 obs[2] + menor_t * vet[2]])
    normal = ponto_intersecao - centro
    return True, menor_t, normal

def intersecao_plano(pla, vet, obs):
    try:
        it = (np.dot(pla[1], obs) - np.dot(pla[1], pla[2]))/np.dot(pla[1], vet)
        return True, it, pla[1]
    except EOFError:
        return False, -1, None
