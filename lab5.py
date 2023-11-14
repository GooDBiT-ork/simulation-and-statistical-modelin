import numpy as np

A = np.array([[0.1, 0.2, 0.3], 
              [0.2, 0.2, 0.1],
              [0.1, 0.1, 0]])

f = np.array([1, 2, 3])

# Начальное приближение   
x0 = np.zeros(3) 

# Параметры моделирования
n_iter = 10000
transition_prob = 0.5*np.ones((3,3)) + 0.5*np.eye(3)

for i in range(n_iter):
    x = np.random.choice(range(3), p=transition_prob[x0]) 
    w = f - np.dot(A, x)
    x0 = x

x_mc = np.average(x, weights=w)

# Точное решение
from numpy.linalg import solve
x_exact = solve(A, f)

print(x_mc)
print(x_exact)