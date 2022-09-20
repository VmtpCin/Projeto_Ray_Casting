import numpy as np
from skspatial.objects import Sphere, Line, Plane


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
    esfera = Sphere(esf[1], esf[2])
    try:
        p1, p2 = esfera.intersect_line(Line(obs, vet))
    except ValueError:
        return '', ''
    return p1, p2


def intersecao_plano(pla, vet, obs):
    plano = Plane(pla[2], pla[1])
    try:
        p = plano.intersect_line(Line(obs, vet))
    except ValueError:
        return ''
    return p
