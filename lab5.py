import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

# Ваша система уравнений
A = np.array([[1.2, -0.4, 0.3], [0.1, 0.7, -0.2], [-0.4, 0.0, 1.4]])
f = np.array([1, 2, -2])

# Решение системы уравнений с помощью встроенной функции
sol_scipy = solve(A, f)

# Метод Монте-Карло
def monte_carlo(A, f, N_chain, N_iter):
    n = len(f)
    x = np.zeros(n)
    Q = np.tril(A)
    R = A - Q
    for _ in range(N_chain):
        x_temp = np.zeros(n)
        for _ in range(N_iter):
            x_temp = np.dot(np.linalg.inv(Q), f - np.dot(R, x_temp))
        x += x_temp
    return x / N_chain

# Параметры для метода Монте-Карло
N_chain = 100
N_iter = 1000

# Решение системы уравнений методом Монте-Карло
sol_mc = monte_carlo(A, f, N_chain, N_iter)

# Сравнение решений
print("Решение, полученное с помощью встроенной функции:", sol_scipy)
print("Решение, полученное с помощью метода Монте-Карло:", sol_mc)

# График зависимости точности решения от длины цепи Маркова
errors = []
N_iters = range(100, 2000, 100)
for Ni in N_iters:
    sol_mc_i = monte_carlo(A, f, N_chain, Ni)
    error = np.linalg.norm(sol_scipy - sol_mc_i)
    errors.append(error)
plt.figure()
plt.plot(N_iters, errors)
plt.xlabel('Длина цепи Маркова')
plt.ylabel('Ошибка')
plt.title('Зависимость точности решения от длины цепи Маркова')
plt.show()


# # Построение графика
# plt.figure(figsize=(10, 6))
# plt.plot(chain_lengths, errors, marker='o')
# plt.title('Зависимость точности решения от длины цепи Маркова')
# plt.xlabel('Длина цепи Маркова')
# plt.ylabel('Ошибка')
# plt.grid(True)
# plt.show()


