import numpy as np

def monte_carlo_solver(matrix, vector, iterations):
    n = len(matrix)
    x = np.zeros(n)  # начальное приближение для решения

    for _ in range(iterations):
        random_vector = np.random.rand(n)  # генерация случайного вектора
        delta_f = vector - np.dot(matrix, x)  # разность между исходным вектором и текущим приближением
        delta_x = np.linalg.solve(matrix, delta_f)  # решение системы линейных уравнений для разности
        x += np.dot(random_vector, delta_x)  # обновление текущего приближения

    return x

matrix = np.array([[1.2, -0.4, 0.3], [0.1, 0.7, -0.2], [-0.4, 0, 1.4]])
vector = np.array([1, 2, -2])
iterations = 1000

solution = monte_carlo_solver(matrix, vector, iterations)
print("Решение системы линейных уравнений:", solution)
