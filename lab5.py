import numpy as np
from random import uniform
from scipy.linalg import eigvals,solve


def solve(size, chain_length, matrix,f):
    m = size * 1000 
    
    h = np.eye(size) 
    pi = np.ones_like(f) * (1.0 / size) # Вектор вероятностей начальных состояний цепи Маркова
    P = np.array(np.ones_like(matrix)) * (1 / size) # Матрица переходов
    
    ksi = np.zeros((m, size), dtype=float)
    idxs = np.array(np.random.rand(m, chain_length) // (1 / size), dtype=int)
    Q = np.zeros((m, chain_length, size), dtype=float)

    for j in range(m):
        idx = idxs[j][0]
        Q[j][0][idx] = 0 if not pi[idx] else h[idx, idx] / pi[idx]
        for k in range(1, chain_length):
            old_state = idxs[j][k - 1]
            new_state = idxs[j][k]
            Q[j][k][idx] = (
                0 if not P[old_state][new_state]
                else Q[j][k - 1][idx] * matrix[old_state][new_state] / P[old_state][new_state]
            )

        ksi[j] = np.dot(f[idxs[j]], Q[j])

    return ksi.mean(axis=0)

matrix = [[1.2,-0.4,0.3],[0.1,0.7,-0.2],[-0.4,0,1.4]]
f = np.array([1,2,-2])

print(solve(3, 1000, matrix,f))
print("Точное решение: ", np.linalg.solve(matrix, f))