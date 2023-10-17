import random
import  matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import chi2
import math
import numpy as np

def MMG(b_array, c_array, k):
    n = len(b_array)
    a = []
    V = list(b_array[0:k])
    for i in range(n):
        s = (int)(c_array[i]*k)
        a.append(V[s])
        if (i + k < n):
            V[s] = b_array[i + k]
    return a
# Мультипликативный конгруэнтный метод
def MCG(beta, alpha, M, n):
    outSeq = []
    xCurr = alpha
    for i in range(n):
        xCurr = (beta * xCurr) % M
        outSeq.append(xCurr / M)
    return outSeq

def RG(n):
    a = []
    for i in range(n):
        a.append(random.random())
    return a



beta = 29791  
alpha = 29791
m = 2**31
k = 128
n = 1000

mcg_sample = MCG(beta,alpha,m,n)
rg_sample = RG(n)
mmg_sample = MMG(mcg_sample,rg_sample,k)

def Pirson(a_, L):
    a = list(a_[:])
    a.sort()
    n = len(a)
    i = 0
    count = 0
    xi2 = 0
    for l in range(1,L+1):
        count = 0
        while ((a[i] < float(l/L)) and (i<n-1)):
            i+=1
            count+=1
        xi2+=pow(count - float(n/L), 2)/n*L
    return xi2

def Kolmogorov(a_):
    a = list(a_[:])
    a.sort()
    n = len(a)
    Dn = 0
    tmp = 0
    for i in range(n):
        tmp = abs(float(i+1)/n - a[i])
        if(tmp > Dn):
            Dn = tmp
    return math.sqrt(n)*Dn

print('Pirson for mcg ', Pirson(mcg_sample,10))
print('Pirson for rg ', Pirson(rg_sample,10))
print('Pirson for mmg ', Pirson(mmg_sample,10))

print('Kolmogorov for mcg ', Kolmogorov(mcg_sample))
print('Kolmogorov for rg ', Kolmogorov(rg_sample))
print('Kolmogorov for mmg ', Kolmogorov(mmg_sample))


# Диаграмма рассеяния
plt.subplot (2, 2, 1)
plt.scatter(range(n), mcg_sample, s=1)
plt.title('Диаграмма рассеяния для MCG')

plt.subplot (2, 2, 2)
plt.scatter(range(n), mmg_sample, s=1)
plt.title('Диаграмма рассеяния для MMG')

# Гистограммы
plt.subplot (2, 2, 3)
plt.hist(mcg_sample, bins=n)
plt.title('Гистограмма для MCG')

plt.subplot (2, 2, 4)
plt.hist(mmg_sample, bins=n) 
plt.title('Гистограмма для MMG')
plt.show()