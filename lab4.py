
import random
import scipy.integrate as integrate
import numpy as np
import  matplotlib.pyplot as plt

def function_a(x):
    return (np.exp(x))*np.log(x)

def function_b(x,y):
    return np.exp(-(x*x+y*y)/2)*np.log(1+(2*x-3*y)**2)

def function_b2(x,y):
    return np.log(1+(2*x-3*y)**2)

def integral_a(function, a, b, n):
    return sum([function(a+(b-a)*random.random()) for _ in range(n)]) * (b - a) / n

def generate_samples(generate_sample, n=1000, **kwargs):
    return np.array([generate_sample(**kwargs) for _ in range(n)])

def normal_sample(N=12, loc=0, scale=1):
    sum = 0 
    for i in range(0, N):
        sum += random.random()
    return loc + (12 / N) ** 0.5 * (sum - N / 2) * scale

def integral_b(function,n):
    m = 0
    s2 = 1
    s = s2 ** 0.5
    normalx = []
    normaly = []
    temp = 0
    result = 0
    normalx = generate_samples(normal_sample, n, loc=m, scale=s)
    normaly = generate_samples(normal_sample, n, loc=m, scale=s)
    for i in range(n):
        temp = 2*(np.pi)*function(normalx[i],normaly[i])
        result += temp
    return result/n


N = 10000
mc1 = list()
I1 = integrate.quad(function_a, 1, 3)[0]
math1 = [I1 for _ in range(1,N)]
for n in range(1,N):
    mc1.append(integral_a(function_a, 1, 3, n))

plt.scatter(range(1,N),math1,s=1)
plt.scatter(range(1,N),mc1,s=1)
plt.title('I1')
plt.show()

N = 2000
mc2 = list() 
I2 = integrate.dblquad(function_b, -np.inf, np.inf, lambda x : -np.inf,lambda x : np.inf)[0]
math2 = [I2 for _ in range(1,N,15)] 
for n in range(1,N,15):
    mc2.append(integral_b(function_b2,n))

plt.scatter(range(1,N,15),math2,s=1)
plt.scatter(range(1,N,15),mc2,s=1)
plt.title('I2')
plt.show()





