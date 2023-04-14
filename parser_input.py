

"""
    ponto_observador = np.array(transformar_em_lista(input(''))) = 0 0 0
    ponto_alvo = np.array(transformar_em_lista(input(''))) = 1 0 0
    vetor_up = np.array(transformar_em_lista(input(''))) = 0 1 0
    angulo_de_visao = int(input('')) = X
    distancia_objeto_tela = int(input('')) = 1
    pixels_largura_k = int(input('')) = 300
    pixels_altura_m = int(input('')) = 200
    
    0   1   2    3   4 5 6   7 8 9  10 11 12
    c [300 200] [1] [0 1 0] [0 0 0] [1 0 0]
    c 300 200 1 0 1 0 0 0 0 0 1 0 0

    0  1 2 3   4
    s [2 0 0] [1] 200 10 150 1 1 0.5 0.5 0.5 3

    0 1 2  3  4 5 6
    p 2 0 -10 1 0 0 200 10 10 1 0.5 0.5 0.5 0.5 3
"""
import os

import numpy as np


class Camera:
    def __init__(self, altura: int, largura: int, distancia: int, vetor_up: np.ndarray,
                 ponto_observador: np.ndarray, ponto_alvo: np.ndarray):
        self.altura = altura
        self.largura = largura
        self.distancia = distancia
        self.vetor_up = vetor_up
        self.ponto_observador = ponto_observador
        self.ponto_alvo = ponto_alvo
    
    def __str__(self) -> str:
        return f"Camera[{self.altura}, {self.largura}, {self.distancia}, {self.vetor_up}, {self.ponto_observador}, {self.ponto_alvo}]"

class Material:
    def __init__(self, v_or: float, og: float, ob: float, kd: float, ks: float, ka: float, kr: float, kt: float, p: float):
        self.values = [v_or, og, ob, kd, ks, ka, kr, kt, p]
    
    def __str__(self):
        return f"Material[{self.values}]"

class Sphere:
    def __init__(self, centro: np.ndarray, raio: int, material: Material):
        self.centro = centro
        self.raio = raio
        self.material = material
    
    def __str__(self) -> str:
        return f"Sphere[{self.centro}, {self.raio}, {self.material}]"

class Plane:
    def __init__(self, normal: np.ndarray, ponto: np.ndarray, material: Material):
        self.normal = normal
        self.ponto = ponto
        self.material = material
    
    def __str__(self):
        return f"Plane[{self.normal}, {self.ponto}, {self.material}]"

class Light:
    def __init__(self, ponto: np.ndarray, intensidade: list[int]):
        self.ponto = ponto
        self.intensidade = intensidade
    
    def __str__(self) -> str:
        return f"Light[{self.ponto}, {self.intensidade}]"

class Ambiente:
    def __init__(self, intensidade: np.ndarray):
        self.intensidade = intensidade

    def __str__(self) -> str:
        return f"Ambiente[{self.intensidade}]"

class ParserInput:
    def __init__(self, filename: str):
        self.objetos_index = 0
        self.objetos = {}
        self.luzes_index = 0
        self.luzes = {}
        self.ambiente_index = 0
        self.ambiente = {}
        self.read_file(filename)

    def read_file(self, filename: str) -> None:
        triangle_counter = 0
        should_skip = False
        with open(filename, "r") as file:
            for line in file.readlines():
                content = line.removesuffix('\n').split(' ')

                if should_skip:
                    triangle_counter -= 1
                    if triangle_counter == 0:
                        should_skip = False
                    continue

                if content[0] == 'c':
                    self.camera = Camera(
                        int(content[2]),
                        int(content[1]),
                        int(content[3]),
                        np.array([int(content[4]), int(content[5]), int(content[6])]), 
                        np.array([int(content[7]), int(content[8]), int(content[9])]), 
                        np.array([int(content[10]), int(content[11]), int(content[12])])
                    )
                if content[0] == 's':
                    sphere = Sphere(
                        np.array([int(content[1]), int(content[2]), int(content[3])]), 
                        int(content[4]),
                        Material(float(content[5]), float(content[6]),float(content[7]), float(content[8]), float(content[9]), float(content[10]), float(content[11]), float(content[12]), float(content[13])),
                    )
                    self.objetos[self.objetos_index] = ['Esfera', sphere.raio, sphere.centro, sphere.material.values]
                    self.objetos_index += 1
                if content[0] == 'p':
                    plane = Plane(
                        np.array([int(content[4]), int(content[5]), int(content[6])]),
                        np.array([int(content[1]), int(content[2]), int(content[3])]),
                        Material(float(content[7]), float(content[8]),float(content[9]), float(content[10]), float(content[11]), float(content[12]), float(content[13]), float(content[14]), float(content[15])),
                    )
                    self.objetos[self.objetos_index] = ['Plano', plane.normal, plane.ponto, plane.material.values]
                    self.objetos_index += 1
                if content[0] == 'l':
                    light = Light(
                        np.array([int(content[1]), int(content[2]), int(content[3])]),
                        [int(content[4]), int(content[5]), int(content[6])]
                    )
                    self.luzes[self.luzes_index] = [light.ponto, light.intensidade]
                    self.luzes_index += 1
                if content[0] == 'a':
                    ambiente = Ambiente(
                        np.array([int(content[1]), int(content[2]), int(content[3])]),
                    )
                    self.ambiente[self.ambiente_index] = [ambiente.intensidade]
                    self.ambiente_index += 1
                if content[0] == 't':
                    triangle_counter = int(content[1]) + int(content[2])
                    should_skip = True


if __name__ == '__main__':
    pi = ParserInput("input.txt")
    print(pi.camera)
    print(pi.objetos)
    print(pi.luzes)
    print(pi.ambiente)