import numpy as np
from skspatial.objects import Sphere, Line, Plane
from math import sqrt


def registrar_objetos():
    objetos = {}
    objeto = []
    num_de_objetos = int(input(''))
    for i in range(num_de_objetos):
        tipo = input('')
        if tipo == '1':
            raio = int(input(''))
            centro = input('')
            objeto = ['Esfera', raio, centro]
            objetos[i] = objeto
        elif tipo == '2':
            vetor_normal_plano = input('')
            ponto = input('')
            objeto = ['Plano', vetor_normal_plano, ponto]
            objetos[i] = objeto
    return objetos


def intersecao_esfera(esf, vet, obs):
    a = np.linalg.norm(vet)**2
    b = 2 * (np.dot(vet, obs) - np.dot(vet, esf[2]))
    c = np.linalg.norm(obs) - (2 * np.dot(esf[2], obs)) + np.linalg.norm(esf[2])**2 - esf[1]**2
    delta = b**2 - (4*a*c)
    if delta < 0:
        return 'Não existe'
    it1 = (-b + sqrt(delta))/2*a
    it2 = (-b - sqrt(delta))/2*a
    if it1 < it2:
        menor_t = it1
    else:
        menor_t = it2
    x = obs[0] + menor_t * vet[0]
    y = obs[1] + menor_t * vet[1]
    z = obs[2] + menor_t * vet[2]
    return np.array([x, y, z])


def intersecao_plano(pla, vet, obs):
    it = (np.dot(pla[1], obs) - np.dot(pla[1], pla[2]))/np.dot(pla[1], vet)
    x = obs[0] + it * vet[0]
    y = obs[1] + it * vet[1]
    z = obs[2] + it * vet[2]
    return np.array([x, y, z])
