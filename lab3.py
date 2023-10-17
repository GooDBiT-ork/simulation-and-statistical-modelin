import numpy as np
import seaborn as sns
from scipy.stats import kstwobign
from scipy.special import erf
import random

sns.set(rc = {'figure.figsize':(15,8)})
sns.set_theme(style='whitegrid', palette='dark:#5A9_r')

np.random.seed(42)

# Критерий Колмогорова
def ks_test(samples, cdf, alpha=0.05, **kwargs):
    n = len(samples)
    empirical_cdf = np.arange(n) / n
    theoretical_cdf = np.array([cdf(x, **kwargs) for x in sorted(samples)])
    Dn = np.max(np.abs(theoretical_cdf - empirical_cdf))
    ks_value = np.sqrt(n) * Dn

    significance_level = 1 - alpha
    critical_value = kstwobign.ppf(significance_level)

    print(
        f"Критерий Колмогорова",
        "\nH0: различий между тестируемыми выборками нет, как и различий между их распределениями.",
        "\nУровень доверия: ", significance_level
    )
    if ks_value < critical_value:
        print(f"H0 принята: {ks_value} < {critical_value}.")
    else:
        print(f"H0 не принята: {ks_value} >= {critical_value}.")


# Генерация выборки на ГММ
def generate_samples(generate_sample, n=1000, **kwargs):
    return np.array([generate_sample(**kwargs) for _ in range(n)])


# #### нормальное распределение на ГММ и встроенном генераторе
def normal_sample(N=12, loc=0, scale=1):
    sum = 0 
    for i in range(0, N):
        sum += np.random.rand()
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

ks_test(normal, normal_cdf, loc=m, scale=s)

sns.histplot(normal, kde=True, linewidth=0)


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

ks_test(lognormal, lognormal_cdf, loc=m, scale=s)

sns.histplot(lognormal, kde=True, linewidth=0)


# #### Логистическое распределение на ГММ и встроенном генераторе
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

ks_test(logistic, logistic_cdf, loc=mu, scale=k)

sns.histplot(logistic, kde=True, linewidth=0)