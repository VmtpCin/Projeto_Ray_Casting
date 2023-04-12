import numpy as np
from math import sqrt


def transformar_em_lista(string):
    vetor = string.split(' ')
    for g in range(3):
        vetor[g] = int(vetor[g])
    return vetor


class Objetos:

    def __init__(self):
        self.objetos = []
        self.luzes = []
        self.ambiente = []
        self.camera = []

    def return_camera(self):
        return self.camera

    def register(self, line):
        line = line.split(" ")
        tipo = line[0]
        for a in range(1, len(line)):
            line[a] = float(line[a])
        if tipo == 's':
            raio = line[4]
            centro = np.array([line[1], line[2], line[3]])
            mtrl = np.array([line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13]])
            objeto = ['Esfera', raio, centro, mtrl]
            self.objetos.append(objeto)
        elif tipo == 'p':
            vetor_normal_plano = np.array([line[4], line[5], line[6]])
            ponto = np.array([line[1], line[2], line[3]])
            mtrl = np.array([line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15]])
            objeto = ['Plano', vetor_normal_plano, ponto, mtrl]
            self.objetos.append(objeto)
        elif tipo == 'c':
            hres = line[1]
            vres = line[2]
            d = line[3]
            up = np.array([line[4], line[5], line[6]])
            origem = np.array([line[7], line[8], line[9]])
            alvo = np.array([line[10], line[11], line[12]])
            objeto = ['Camera', hres, vres, d, up, origem, alvo]
            self.camera = objeto
        elif tipo == 'l':
            ponto = np.array([line[1], line[2], line[3]])
            intensidade = np.array([line[4], line[5], line[6]])
            luz = [ponto, intensidade]
            self.luzes.append(luz)
        elif tipo == 'a':
            intensidade = np.array([line[1], line[2], line[3]])
            self.ambiente = np.array(intensidade)
        # elif tipo == 't':
        return 0

    def intersect(self, vet, obs):
        men_t = 999999999999
        primeira_interseccao = -1
        for i in range(len(self.objetos)):
            if self.objetos[i][0] == 'Esfera':
                inter, t, p, mtrl, n = self.intersecao_esfera(self.objetos[i], vet, obs)
                if inter is True and t < men_t:
                    men_t = t
                    return inter, t, p, mtrl, n
            elif self.objetos[i][0] == 'Plano':
                inter, t, p, mtrl, n = self.intersecao_plano(self.objetos[i], vet, obs)
                if inter is True and t < men_t:
                    men_t = t
                    return inter, t, p, mtrl, n

        return False, -1, 0, 0, 0

    def intersecao_esfera(self, esf, vet, obs):
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

        if it1 < 0 and it2 < 0:
            return False, -1, 0, 0, 0
        else:
            x = obs[0] + menor_t * vet[0]
            y = obs[1] + menor_t * vet[1]
            z = obs[2] + menor_t * vet[2]
            ponto = np.array([x, y, z])
            normal = ponto - obs
            return True, menor_t, ponto, esf[3], normal

    def intersecao_plano(self, pla, vet, obs):
        try:
            it = (np.dot(pla[1], obs) - np.dot(pla[1], pla[2]))/np.dot(pla[1], vet)
            return True, it
        except EOFError:
            return False, -1

        # x = obs[0] + it * vet[0]
        # y = obs[1] + it * vet[1]
        # z = obs[2] + it * vet[2]
        # return np.array([x, y, z])
