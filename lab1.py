import random
import  matplotlib.pyplot as plt
import scipy.stats as stats
import math

# Мультипликативный конгруэнтный метод
def MCM_RNG(seed, a, m, size):
    if size==1:
        return math.ceil(math.fmod(a*seed,m))
    r=[0 for i in range(size)]
    r[0]=seed
    for i in range(1,size):
        r[i]=math.ceil(math.fmod((a*r[i-1]),m))
    return r[1:size]

# Линейный конгруэнтный метод
def LCM_RNG(seed, a, c, m, size):
    if size==1:
        return math.ceil(math.fmod(a*seed + c,m))
    r=[0 for i in range(size)]
    r[0]=seed
    for i in range(1,size):
        r[i]=math.ceil(math.fmod((a*r[i-1] + c),m))
    return r[1:size]

# Метод Макларена-Марсальи 
# Датчик 1 - мультипликативный конгруэнтный метод
# Датчик 2 - линейный конгруэнтный метод   
def MM_RNG(seed, a, c, m, size):
    x = MCM_RNG(seed, a, m, size) # Датчик 1
    y = LCM_RNG(seed, a, c, m, size) # Датчик 2
    return x ^ y

a = 29791  
seed = 29791
c = 17
m = 2**31
k = 128
n = 1000

# Моделирование МКМ
mkm_sample = MCM_RNG(seed, a, m, n)

# Моделирование Макларена-Марсальи
mm_sample = MM_RNG(seed, a, c, m, n)

# Проверка равномерности МКМ
mkm_stat, mkm_p = stats.kstest(mkm_sample,'uniform', N=n)
print('Статистика К-С для МКМ:', mkm_stat)
print('p-значение К-С для МКМ:', mkm_p)

mkm_chi2, mkm_p = stats.chisquare(mkm_sample)
print('Статистика хи-квадрат для МКМ:', mkm_chi2)
print('p-значение хи-квадрат для МКМ:', mkm_p)

# Проверка равномерности ММ
mm_stat, mm_p = stats.kstest(mm_sample,'uniform', N=n)
print('Статистика К-С для ММ:', mm_stat) 
print('p-значение К-С для ММ:', mm_p)

mm_chi2, mm_p = stats.chisquare(mm_sample)
print('Статистика хи-квадрат для ММ:', mm_chi2)
print('p-значение хи-квадрат для ММ:', mm_p)

# Диаграмма рассеяния
plt.subplot (2, 2, 1)
plt.scatter(range(n), mkm_sample, s=1)
plt.title('Диаграмма рассеяния для МКМ')

plt.subplot (2, 2, 2)
plt.scatter(range(n), mm_sample, s=1)
plt.title('Диаграмма рассеяния для ММ')

# Гистограммы
plt.subplot (2, 2, 3)
plt.hist(mkm_sample, bins=50)
plt.title('Гистограмма для МКМ')

plt.subplot (2, 2, 4)
plt.hist(mm_sample, bins=50) 
plt.title('Гистограмма для ММ')
plt.show()