import math
import numpy as np

# constabtes da transformação linear
X = 1
Y = 1
Z = 1

# constabtes da transformação linear
LX = 1
LY = 1
LZ = 1

# matriz da transformação obrigatoria
obrig = [
    [math.cos(math.radians(30)), - math.sin(math.radians(30)), 0, 0],
    [math.sin(math.radians(30)), math.cos(math.radians(30)), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]


# multiplicar matrizes
def matriz_multi(matriz, outra):
    result = [0, 0, 0, 0]
    for i in range(len(outra)):
        for j in range(len(outra)):
            result[i] += outra[i] * matriz[j][i]

    return result


# print(matriz_multi(obrigatoria,[1,1,1,1]))

class Transforma:

    def tlinear(self, vector):
        return [vector[0] * LX, vector[1] * LY, vector[2] * LZ]

    def tinverse_linear(self, vector):
        return [vector[0] / LX, vector[1] / LY, vector[2] / LZ]

    def translatar1(self, vector, vec_point, trans):
        array = [vector[0], vector[1], vector[2], vec_point]

        matrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [X * trans, Y * trans, Z * trans, 1]
        ]

        return np.array(matriz_multi(matrix, array))

    def translatar2(self, vector, vec_point):
        array = [vector[0], vector[1], vector[2], vec_point]

        matrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [X, Y, Z, 1]
        ]

        return np.array(matriz_multi(matrix, array))

    def rotacionar(self, vector):

        vetor = self.translatar1(vector, 1, -1)
        vetor = [vetor[0], vetor[1], vetor[2], 1]
        vetor = matriz_multi(obrig, vetor)
        vetor.pop(3)
        vetor = self.translatar1(vector, 1, 1)

        return vetor

