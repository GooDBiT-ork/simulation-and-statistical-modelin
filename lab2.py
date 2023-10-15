#Биномиальное – Bi(m,p), m = 6, p = 0.75; Геометрическое – G(p), p = 0.7; 
import random
import  matplotlib.pyplot as plt
import math

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

p_geom = 0.7
n = 1000

def gen_geom(p):
    a = random.random()
    return math.floor(math.log(a) / math.log(1 - p)) + 1

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
    result = list()
    x = 0
    for j in range(m):
        if random.random() < p:
            x += 1
    result.append(x)
    return result

e_exp_binom = m_binom*p_binom
d_exp_binom = m_binom*p_binom*(1-p_binom)

print('Несмещенные МО и Д биномиального распределения:\n', 'МО - ',e_exp_binom, '\n','Д - ',d_exp_binom)

val_binom = list()
for i in range(n):
    val_binom.append(gen_geom(p_geom))
    
e_obs_binom = get_expectation(val_binom)
d_obs_binom = get_dispersion(val_binom)

print('Истинные значения МО и Д биномиального распределения:\n', 'МО - ',e_obs_binom, '\n','Д - ',d_obs_binom)





plt.subplot (2, 2, 1)
plt.scatter(range(n), val_geom, s=1)
plt.title('Диаграмма рассеяния для ГР')

plt.subplot (2, 2, 2)
plt.scatter(range(n), val_binom, s=1)
plt.title('Диаграмма рассеяния для БР')

# Гистограммы
plt.subplot (2, 2, 3)
plt.hist(val_geom, bins=n)
plt.title('Гистограмма для ГР')

plt.subplot (2, 2, 4)
plt.hist(val_binom, bins=n) 
plt.title('Гистограмма для БР')
plt.show()

