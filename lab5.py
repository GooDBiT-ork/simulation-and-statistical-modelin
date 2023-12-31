import numpy as np
import matplotlib.pyplot as plt

def mc_simulation(n,N,m,a,f,h):
    pi = np.array([1/n, 1/n, 1/n])
    p = np.array([[1/n, 1/n, 1/n], [1/n, 1/n, 1/n], [1/n, 1/n, 1/n]])
    i = np.zeros(N+1, dtype=int)
    Q = np.zeros(N+1)
    ksi = np.zeros(m)


    for j in range(m):
        alpha = np.random.rand()
        if alpha < pi[0]:
            i[0] = 0
        elif alpha < pi[0] + pi[1]:
            i[0] = 1
        else:
            i[0] = 2

        for k in range(1, N+1):
            alpha = np.random.rand()
            if alpha < p[i[k-1]][0]:
                i[k] = 0
            elif alpha < p[i[k-1]][0] + p[i[k-1]][1]:
                i[k] = 1
            else:
                i[k] = 2

        if pi[i[0]] > 0:
            Q[0] = h[i[0]] / pi[i[0]]
        else:
            Q[0] = 0

        for k in range(1, N+1):
            if p[i[k-1]][i[k]] > 0:
                Q[k] = Q[k-1] * a[i[k-1]][i[k]] / p[i[k-1]][i[k]]
            else:
                Q[k] = 0

        for k in range(N+1):
            ksi[j] += Q[k] * f[i[k]]

    return np.mean(ksi)



def monte_carlo_solution(n,N,m,a,f):
    # h = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # pi = np.array([1/n, 1/n, 1/n])
    # p = np.array([[1/n, 1/n, 1/n], [1/n, 1/n, 1/n], [1/n, 1/n, 1/n]])
    # i = np.zeros(N+1, dtype=int)
    # Q = np.zeros((N+1, n))  
    # ksi = np.zeros((m, n))  

    # for j in range(m):
    #     alpha = np.random.rand()
    #     if alpha < pi[0]:
    #         i[0] = 0
    #     elif alpha < pi[0] + pi[1]:
    #         i[0] = 1
    #     else:
    #         i[0] = 2

    #     for k in range(1, N+1):
    #         alpha = np.random.rand()
    #         if alpha < p[i[k-1]][0]:
    #             i[k] = 0
    #         elif alpha < p[i[k-1]][0] + p[i[k-1]][1]:
    #             i[k] = 1
    #         else:
    #             i[k] = 2

    #     if pi[i[0]] > 0:
    #         Q[0] = h[i[0]] / pi[i[0]]
    #     else:
    #         Q[0] = 0

    #     for k in range(1, N+1):
    #         if p[i[k-1]][i[k]] > 0:
    #             Q[k] = Q[k-1] * a[i[k-1]][i[k]] / p[i[k-1]][i[k]]
    #         else:
    #             Q[k] = 0

    #     for k in range(N+1):
    #         ksi[j] += Q[k] * f[i[k]]

    # return np.mean(ksi, axis=0)
    return [mc_simulation(n,N,m,a,f,[1,0,0]),mc_simulation(n,N,m,a,f,[0,1,0]),mc_simulation(n,N,m,a,f,[0,0,1])]

A_v7 = np.array([[1.2, -0.4, 0.3], [0.1, 0.7, -0.2], [-0.4, 0.0, 1.4]])
a_v7 = np.array([[-0.2, 1.4, 0.7], [0.9, 0.3, 1.2], [1.4, 1.0, -0.4]])
A = np.array([[0.5, 0, 0], [0, 0.3, 0], [0, 0, 0.7]])
a = np.array([[0.5, 0, 0], [0, 0.7, 0], [0, 0, 0.3]])
f = np.array([1, 2, -2])
size = len(f)
exact_solution = np.linalg.solve(A, f)
print(f'exact_solution = {exact_solution}')

num_chains1 = 500
chain_lengths1 = np.arange(1000, 10000, 100)
errors1 = []
for chain_length in chain_lengths1:
    monte_carlo_solve = monte_carlo_solution(size,num_chains1,chain_length,a,f)
    print(monte_carlo_solve)
    error = np.linalg.norm(monte_carlo_solve - exact_solution)
    errors1.append(error)

num_chains2 = np.arange(1000, 10000, 100)
chain_lengths2 = 1000
errors2 = []
for num_chain in num_chains2:
    monte_carlo_solve = monte_carlo_solution(size,num_chain,chain_lengths2,a,f)
    print(monte_carlo_solve)
    error = np.linalg.norm(monte_carlo_solve - exact_solution)
    errors2.append(error)
    

plt.figure(figsize=(10, 6))
plt.plot(chain_lengths1, errors1, marker='o')
plt.title('Зависимость точности решения от длины цепи Маркова')
plt.xlabel('Длина цепи Маркова')
plt.ylabel('Ошибка')
plt.grid(True)
plt.show()
 
plt.figure(figsize=(10, 6))
plt.plot(num_chains2, errors2, marker='o')
plt.title('Зависимость точности решения от кол-во цепей Маркова')
plt.xlabel('Длина цепи Маркова')
plt.ylabel('Ошибка')
plt.grid(True)
plt.show()

monte_carlo_solve = monte_carlo_solution(size,5000,10000,a,f)
print(f'monte_carlo_solve = {monte_carlo_solve}')
