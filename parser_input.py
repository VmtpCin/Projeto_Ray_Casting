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
    def __init__(self, v_or: float, og: float, ob: float, kd: float, ks: float, ka: float, kr: float, kt: float,
                 p: float, refracao: float):
        self.values = [v_or, og, ob, kd, ks, ka, kr, kt, p, refracao]

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


class Triangle:
    def __init__(self, point1: np.ndarray, point2: np.ndarray, point3: np.ndarray, indexes: list[int]):
        self.ponto1 = point1
        self.ponto2 = point2
        self.ponto3 = point3
        self.indexes = indexes
        self.normal = np.cross((self.ponto1 - self.ponto2), (self.ponto1 - self.ponto3))

    def __str__(self):
        return f"Triangle[{self.ponto1}, {self.ponto2}, {self.ponto3}, {self.normal}]"

    def contains(self, vertice):
        return (vertice == self.ponto1).all() or (vertice == self.ponto2).all() or (vertice == self.ponto3).all()


class Light:
    def __init__(self, ponto: np.ndarray, intensidade: float, tipo: str):
        self.ponto = ponto
        self.intensidade = intensidade
        self.tipo = tipo

    def __str__(self) -> str:
        return f"Light[{self.ponto}, {self.intensidade}, {self.tipo}]"


class Ambiente:
    def __init__(self, intensidade: float):
        self.intensidade = intensidade

    def __str__(self) -> str:
        return f"Ambiente[{self.intensidade}]"


class ParserInput:
    def __init__(self, filename: str):
        self.objetos_index = 0
        self.objetos = {}
        self.luzes = []
        self.ambiente = 0.0
        self.read_file(filename)

    def read_file(self, filename: str) -> None:
        n_vertices = 0
        n_triangles = 0
        read_mesh_material = False
        vertices = []
        triangles = []

        with open(filename, "r") as file:
            for line in file.readlines():
                content = line.removesuffix('\n').split(' ')

                if content[0] == 'c':
                    camera = Camera(
                        int(content[2]),
                        int(content[1]),
                        int(content[3]),
                        np.array([int(content[4]), int(content[5]), int(content[6])]),
                        np.array([int(content[7]), int(content[8]), int(content[9])]),
                        np.array([int(content[10]), int(content[11]), int(content[12])])
                    )
                    self.camera = [camera.ponto_observador, camera.ponto_alvo, camera.vetor_up, -1, camera.distancia,
                                   camera.largura, camera.altura]
                if content[0] == 's':
                    sphere = Sphere(
                        np.array([int(content[1]), int(content[2]), int(content[3])]),
                        int(content[4]),
                        Material(float(content[5]), float(content[6]), float(content[7]), float(content[8]),
                                 float(content[9]), float(content[10]), float(content[11]), float(content[12]),
                                 float(content[13]), float(content[14])),
                    )
                    self.objetos[self.objetos_index] = ['Esfera', sphere.raio, sphere.centro, sphere.material.values]
                    self.objetos_index += 1
                if content[0] == 'p':
                    plane = Plane(
                        np.array([int(content[4]), int(content[5]), int(content[6])]),
                        np.array([int(content[1]), int(content[2]), int(content[3])]),
                        Material(float(content[7]), float(content[8]), float(content[9]), float(content[10]),
                                 float(content[11]), float(content[12]), float(content[13]), float(content[14]),
                                 float(content[15]), float(content[16])),
                    )
                    self.objetos[self.objetos_index] = ['Plano', plane.normal, plane.ponto, plane.material.values]
                    self.objetos_index += 1
                if content[0] == 'l':
                    light = Light(
                        np.array([int(content[1]), int(content[2]), int(content[3])]),
                        float(content[4]),
                        content[5]
                    )
                    self.luzes.append([light.ponto, light.intensidade, light.tipo])
                if content[0] == 'a':
                    ambiente = Ambiente(
                        float(content[1]),
                    )
                    self.ambiente = ambiente.intensidade
                if content[0] == 't':
                    n_triangles = int(content[1])
                    n_vertices = int(content[2])
                    read_mesh_material = True
                    continue

                if n_vertices != 0:
                    vertices.append(np.array([int(content[0]), int(content[1]), int(content[2])]))
                    n_vertices -= 1
                    if n_vertices == 0:
                        continue
                if n_triangles != 0 and n_vertices == 0:
                    indexes = [int(content[0]) - 1, int(content[1]) - 1, int(content[2]) - 1]
                    triangle = Triangle(
                        vertices[indexes[0]], vertices[indexes[1]], vertices[indexes[2]],
                        indexes
                    )
                    triangles.append(triangle)
                    n_triangles -= 1
                    if n_triangles == 0:
                        continue
                if n_triangles == 0 and read_mesh_material:
                    normal_vertices = []

                    for v in vertices:
                        cont = 0
                        soma_normais_faces_adjacentes = 0
                        for triangle in triangles:
                            if triangle.contains(v):
                                soma_normais_faces_adjacentes += triangle.normal
                                cont += 1
                        normal_vertice = soma_normais_faces_adjacentes / cont
                        normal_vertices.append(normal_vertice)

                    for triangle in triangles:
                        self.objetos[self.objetos_index] = [
                            'triangulo', triangle.ponto1, triangle.ponto2, triangle.ponto3, triangle.normal,
                            triangle.indexes, normal_vertices,
                            [float(content[0]), float(content[1]), float(content[2]), float(content[3]),
                             float(content[4]), float(content[5]), float(content[6]), float(content[7]),
                             float(content[8]), float(content[9])],
                        ]
                        self.objetos_index += 1

                    read_mesh_material = False


if __name__ == '__main__':
    pi = ParserInput("input.txt")
    print(pi.camera)
    print(pi.objetos)
    print(pi.luzes)
    print(pi.ambiente)