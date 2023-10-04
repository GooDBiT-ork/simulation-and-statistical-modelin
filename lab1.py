import random
import  matplotlib.pyplot as plt
import scipy.stats as stats
import math

# Мультипликативный конгруэнтный метод
def MCG(a, x, M, length):
    result = []
    for _ in range(length):
        rd = (a * x) % M
        x = rd
        result.append(x / M)
    return result
# Линейный конгруэнтный метод
def LCG(a, x, c, M, length):
    result = []
    for _ in range(length):
        rd = (a * x + c) % M
        x = rd
        result.append(x / M)
    return result

# Метод Макларена-Марсальи   
def MMG(b_array,c_array,k):
    x = random.choice(b_array)
    y = random.choice(c_array)
    j = math.trunc( y * k )
    if j < 1:
        j = 1
    v = b_array[:k]
    Result = v[j]
    v[j] = x
    return Result

a = 29791  
x0 = 29791
c = 0
m = 2**31
k = 128
n = 1000

mcg_sample = MCG(a,x0,m,n)
lcg_sample = LCG(a,x0,c,m,n)
mmg_sample = []
for i in range(n):
    mmg_sample.append(MMG(mcg_sample,lcg_sample,k))


# Проверка равномерности МКМ
mcm_stat, mcm_p = stats.kstest(mcg_sample, stats.uniform.cdf)
print('Статистика К-С для МКМ:', mcm_stat)
print('p-значение К-С для МКМ:', mcm_p)

mcm_chi2, mcm_p = stats.chisquare(mcg_sample)
print('Статистика хи-квадрат для МКМ:', mcm_chi2)
print('p-значение хи-квадрат для МКМ:', mcm_p)

# # Проверка равномерности ММ
mm_stat, mm_p = stats.kstest(mmg_sample,'uniform', N=n)
print('Статистика К-С для ММ:', mm_stat) 
print('p-значение К-С для ММ:', mm_p)

mm_chi2, mm_p = stats.chisquare(mmg_sample)
print('Статистика хи-квадрат для ММ:', mm_chi2)
print('p-значение хи-квадрат для ММ:', mm_p)

def test_Hi(arr, t, eps):
    intervals = {}
    for i in range(t + 1):
        intervals[(i / 1000, (i + 1) / 1000)] = 0

    for i in arr:
        for interval in intervals:
            if interval[0] <= i and i < interval[1]:
                intervals[interval] += 1

    expected = len(arr) / t

    chi2 = sum([((intervals[i / 1000, (i + 1) / 1000] - expected) ** 2) / expected for i in range(t)])
    delt = stats.chi2.ppf(1 - eps, df=t - 1) # (t - 1) число степеней свободы
    print("хи-квадрат:", chi2)
    print("Критическое значение:", delt)
    return chi2 < delt
print('hi qwerty : ', test_Hi(mcg_sample, n, 0.05))
print('hi qwerty : ', test_Hi(mmg_sample, n, 0.05))
# Диаграмма рассеяния
plt.subplot (2, 2, 1)
plt.scatter(range(n), mcg_sample, s=1)
plt.title('Диаграмма рассеяния для MCG')

plt.subplot (2, 2, 2)
plt.scatter(range(n), mmg_sample, s=1)
plt.title('Диаграмма рассеяния для MMG')

# Гистограммы
plt.subplot (2, 2, 3)
plt.hist(mcg_sample, bins=50)
plt.title('Гистограмма для MCG')

plt.subplot (2, 2, 4)
plt.hist(mmg_sample, bins=50) 
plt.title('Гистограмма для MMG')
plt.show()