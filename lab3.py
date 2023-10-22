import numpy as np
import seaborn as sns
from scipy.stats import kstwobign
from scipy.special import erf
import random
import matplotlib.pyplot as plt
from scipy.stats import chi2
import scipy.stats as stats


pieces = 9
eps = 0.05
_N = 100
# Критерий Пирсона
def PearsonTest(samples, distr, loc=0, s=1, n=1000):
    hi = 0
    frequences = [0] * pieces
    step = abs(max(samples) - min(samples)) / pieces
    for i in range(0, n):
        index = int((samples[i] - min(samples)) / step)
        frequences[index if index < pieces else (pieces - 1)] += 1
    TheLastExpected = 0
    for i in range(0, pieces):
        if i != pieces - 1:
            fk = distr((i + 1) * step + min(samples), loc, s)
            fk1 = distr(i * step + min(samples), loc, s)
            p = fk - fk1
            TheLastExpected += p
        else:
            p = 1 - TheLastExpected
        if n * p != 0:
            hi += (((frequences[i] - n * p) ** 2)*0.5/(n * p))
        else:
            return True
    return [hi, stats.chi2(len(frequences)-1).ppf(1 - eps)]


# Критерий Колмогорова
def ks_test(samples, cdf, alpha=0.05, **kwargs):
    n = len(samples)
    empirical_cdf = np.arange(n) / n
    theoretical_cdf = np.array([cdf(x, **kwargs) for x in sorted(samples)])
    Dn = np.max(np.abs(theoretical_cdf - empirical_cdf))
    ks_value = np.sqrt(n) * Dn
    
    return ks_value,kstwobign.ppf(1 - alpha)


# Генерация выборки
def generate_samples(generate_sample, n=1000, **kwargs):
    return np.array([generate_sample(**kwargs) for _ in range(n)])


#Нормальное распределение
def normal_sample(N=12, loc=0, scale=1):
    sum = 0 
    for i in range(0, N):
        sum += random.random()
    return loc + (12 / N) ** 0.5 * (sum - N / 2) * scale


def normal_cdf(x, loc=0, scale=1):
    return 0.5 * (1 + erf((x - loc) / (scale * 2 ** 0.5)))


N = 24
m = 0
s2 = 16
s = s2 ** 0.5

normal = generate_samples(normal_sample, loc=m, scale=s)

print("Нормальное распределение : ")
print("Теоретическое мат. ожидание:", m)
print("Несмещенная оценка матожидания:", normal.mean())
print("Теоретическая дисперсия:", s2)
print("Несмещенная оценка дисперсии:", normal.var())

ks_res = ks_test(normal, normal_cdf, loc=m, scale=s)
print(f'Kolmogorov test = {ks_res[0]<=ks_res[1]}\n KS_набл = {ks_res[0]}\n KS_стат = {ks_res[1]} ')
p_res = PearsonTest(normal, normal_cdf, m, s)
print(f'Pirson test = {p_res[0]<=p_res[1]}\n P_набл = {p_res[0]}\n P_стат = {p_res[1]} ')

count1 = 0
count2 = 0
for i in range(_N):
    normal = generate_samples(normal_sample, loc=m, scale=s)
    ks_res = ks_test(normal, normal_cdf, loc=m, scale=s)
    p_res = PearsonTest(normal, normal_cdf, m, s)
    if(ks_res[0]>ks_res[1]):
        count1+=1
    if(p_res[0]>p_res[1]):
        count2+=1
print('Ошибка первого рода К = ', count1/_N, 'Ошибка первого рода P = ', count2/_N)

#Логнормальное распределение
def lognormal_sample(N=12, loc=0, scale=1):
    sum = 0
    for i in range(0, 12):
        sum += random.random()
    sum -= 6
    return np.exp(loc + scale * sum)

def lognormal_cdf(x, loc=0, scale=1):
    return 0.5 * (1 + erf((np.log(x) - loc) / (scale * 2 ** 0.5)))

N = 20
m = 2
s2 = 16
s = s2 ** 0.5

lognormal = generate_samples(lognormal_sample, loc=m, scale=s)

print("Логнормальное распределение : ")
print("Теоретическое мат. ожидание:", np.exp(m + s2 / 2))
print("Несмещенная оценка матожидания:", lognormal.mean())
print("Теоретическая дисперсия:", (np.exp(s2) - 1) * np.exp(2 * m + s2))
print("Несмещенная оценка дисперсии:", lognormal.var())

ks_res = ks_test(lognormal, lognormal_cdf, loc=m, scale=s)
print(f'Kolmogorov test = {ks_res[0]<=ks_res[1]}\n KS_набл = {ks_res[0]}\n KS_стат = {ks_res[1]} ')
p_res = PearsonTest(lognormal, lognormal_cdf, m, s)
print(f'Pirson test = {p_res[0]<=p_res[1]}\n P_набл = {p_res[0]}\n P_стат = {p_res[1]} ')

count1 = 0
count2 = 0
for i in range(_N):
    lognormal = generate_samples(lognormal_sample, loc=m, scale=s)
    ks_res = ks_test(lognormal, lognormal_cdf, loc=m, scale=s)
    p_res = PearsonTest(lognormal, lognormal_cdf, m, s)
    if(ks_res[0]>ks_res[1]):
        count1+=1
    if(p_res[0]>p_res[1]):
        count2+=1
print('Ошибка первого рода К = ', count1/_N, 'Ошибка первого рода P = ', count2/_N)

#Логистическое распределение
def logistic_sample(loc=0, scale=1):
    x = random.random()
    return loc + scale * np.log(x / (1 - x))

def logistic_cdf(x, loc=0, scale=1):
    return 1 / (1 + np.exp(-(x - loc) / scale))


mu = 1
k = 1
logistic = generate_samples(logistic_sample, loc=mu, scale=k)

print("Логистическое распределение : ")
print("Теоретическое мат. ожидание:", mu)
print("Несмещенная оценка матожидания:", logistic.mean())
print("Теоретическая дисперсия:", np.pi ** 2 * k ** 2 / 3)
print("Несмещенная оценка дисперсии:", logistic.var())

ks_res = ks_test(logistic, logistic_cdf, loc=mu, scale=k)
print(f'Kolmogorov test = {ks_res[0]<=ks_res[1]}\n KS_набл = {ks_res[0]}\n KS_стат = {ks_res[1]} ')
p_res = PearsonTest(logistic, logistic_cdf, mu, k)
print(f'Pirson test = {p_res[0]<=p_res[1]}\n P_набл = {p_res[0]}\n P_стат = {p_res[1]} ')

count1 = 0
count2 = 0
for i in range(_N):
    logistic = generate_samples(logistic_sample, loc=mu, scale=k)
    ks_res = ks_test(logistic, logistic_cdf, loc=mu, scale=k)
    p_res = PearsonTest(logistic, logistic_cdf, mu, k)
    if(ks_res[0]>ks_res[1]):
        count1+=1
    if(p_res[0]>p_res[1]):
        count2+=1
print('Ошибка первого рода К = ', count1/_N, 'Ошибка первого рода P = ', count2/_N)
# plt.subplot (2, 2, 1)
# sns.histplot(normal, kde=True, linewidth=0)
# plt.title('Нормальное распределение')

# plt.subplot (2, 2, 2)
# sns.histplot(lognormal, kde=True, linewidth=0)
# plt.title('Логнормальное распределение')

# plt.subplot (2, 2, 3)
# sns.histplot(logistic, kde=True, linewidth=0)
# plt.title('Логистическое распределение')
# plt.show()