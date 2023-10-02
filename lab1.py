import random
import  matplotlib.pyplot as plt
import scipy.stats as stats

# Мультипликативный конгруэнтный метод
def MCM_RNG(seed, a, m):
    return (a * seed) % m

# Метод Макларена-Марсальи 
# Датчик 1 - мультипликативный конгруэнтный метод
# Датчик 2 - линейный конгруэнтный метод   
def MM_RNG(seed, a, c, m, k):
    x = MCM_RNG(seed, a, m) # Датчик 1
    y = (seed*c + 1) % k # Датчик 2
    return x ^ y

# Параметры
a = 29791  
c = 17
m = 2**31
k = 128
n = 1000

# Моделирование МКМ
seeds = [random.randint(1, m-1) for i in range(n)]
mkm_sample = [MCM_RNG(seed, a, m) for seed in seeds]

# Моделирование Макларена-Марсальи
seeds = [random.randint(1, m-1) for i in range(n)] 
mm_sample = [MM_RNG(seed, a, c, m, k) for seed in seeds]

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