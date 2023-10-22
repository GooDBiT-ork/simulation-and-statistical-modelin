#Биномиальное – Bi(m,p), m = 6, p = 0.75; Геометрическое – G(p), p = 0.7; 
import random
import  matplotlib.pyplot as plt
import math
from scipy.stats import chi2
import scipy.stats as stats
from random import random, uniform
from math import log

# Оценка МО
def get_expectation(val):
    e_obs = 0
    for x in val:
        e_obs += x 
    e_obs /= len(val)
    return e_obs

# Оценка Дисперсии
def get_dispersion(val):
    d = 0
    mean = 0
    for x in val:
        mean += x
    mean /= len(val)
    for x in val:
        d += (x - mean)**2
    d /= (len(val) - 1)
    return d

p_geom = 0.77
n = 1000
eps = 0.05

def gen_geom(p):
    counter = 0
    while (1 if random() < p else 0) != 1:
        counter += 1
    return counter

#math.floor(math.log(a) / math.log(1 - p)) + 1

e_exp_geom = 1 / p_geom
d_exp_geom = (1 - p_geom) / (p_geom**2)

print('Несмещенные МО и Д геометрического распределения:\n', 'МО - ',e_exp_geom, '\n','Д - ',d_exp_geom)
val_geom = list()
for i in range(n):
    val_geom.append(gen_geom(p_geom))
    
e_obs_geom = get_expectation(val_geom)
d_obs_geom = get_dispersion(val_geom)

print('Истинные значения МО и Д геометрического распределения:\n', 'МО - ',e_obs_geom, '\n','Д - ',d_obs_geom)

m_binom = 6
p_binom = 0.75


def gen_binom(m, p):
    q = 1 - p
    c, r = p / q, uniform(0, 1)
    p = pow(q, m)
    x = 0
    r -= p
    while r >= 0:
        x += 1
        p *= c * (m + 1 - x) / x
        r -= p
    return x

e_exp_binom = m_binom*p_binom
d_exp_binom = m_binom*p_binom*(1-p_binom)

print('Несмещенные МО и Д биномиального распределения:\n', 'МО - ',e_exp_binom, '\n','Д - ',d_exp_binom)

val_binom = list()
for i in range(n):
    val_binom.append(gen_binom(m_binom,p_binom))
    
e_obs_binom = get_expectation(val_binom)
d_obs_binom = get_dispersion(val_binom)

print('Истинные значения МО и Д биномиального распределения:\n', 'МО - ',e_obs_binom, '\n','Д - ',d_obs_binom)

def chisquare(val,n,p):
    freqs = {}
    for x in val:
        if x in freqs:
            freqs[x] += 1
        else:
            freqs[x] = 1
    return [sum(((i-n*(p * ((1 - p) ** i)))**2)*(p * ((1 - p) ** i)/n) for i in freqs.values()),freqs]

print(f'X2Geom набл =  {chisquare(val_geom,n,p_geom)[0]}')

print(f'X2Binom набл =  {chisquare(val_binom,n,p_binom)[0]}')

print('X2Geom stat = ', stats.chi2(len(chisquare(val_geom,n,p_geom)[1])-1).ppf(1 - eps))
print('X2Binom stat = ',stats.chi2(len(chisquare(val_binom,n,p_binom)[1]) - 1).ppf(1 - eps))

N = 1000
count1 = 0
count2 = 0
for i in range(N):
    val1 = []
    for i in range(n):
        val1.append(gen_geom(p_geom))
    val2 = []
    for i in range(n):
        val2.append(gen_binom(m_binom,p_binom))
    if(chisquare(val1,n,p_geom)[0] > stats.chi2(len(chisquare(val1,n,p_geom)[1]) - 1).ppf(1 - eps)):
        count1+=1
    if(chisquare(val2,n,p_binom)[0] > stats.chi2(len(chisquare(val2,n,p_binom)[1]) - 1).ppf(1 - eps)):
        count2+=1
if(count1/N<0.05):
    print('Вероятность ошибки I рода стремится к 0.05 для геометрического распределения')
else:
    print('Вероятность ошибки I рода превышает 0.05 для геометрического распределения')

if(count2/N<0.05):
    print('Вероятность ошибки I рода стремится к 0.05 для биномиального распределения')
else:
    print('Вероятность ошибки I рода превышает 0.05 для биномиального распределения')