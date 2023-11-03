import math 
from random import uniform
import scipy.integrate as integrate
import numpy as np
import  matplotlib.pyplot as plt

def function_a(x):
    return x / math.sqrt(1 - 4 * x**2)


def function_b(x):
    return (x * np.log(x)) / (1 + x ** 3)


def integral_a(function, a, b, n):
    return sum([function(uniform(a, b)) for _ in range(n)]) * (b - a) / n


def integral_b(function, n):
    result = 0
    temp = 1
    left = 0

    while abs(temp) > 10 ** (-7):
        temp = 0
        for _ in range(n):
            c_dot = uniform(left, left + 1)
            temp += function(c_dot)
        temp /= n
        result += temp
        left += 1
      
    return result

N = 1000000
mc1 = list()
math1 = list()
for n in range(100000,N,5000):
    mc1.append(integral_a(function_a, 0, 0.5, n))
    math1.append(integrate.quad(function_a, 0, 0.5)[0])


plt.scatter(range(100000,N,5000),mc1,s=1)
plt.title('I1_imp')
plt.show()

# plt.scatter(range(1,N),math1,s=1)
# plt.title('I1_imp')
# plt.show()

