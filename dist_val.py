import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

def cool_dist_u(path, initial_u_values):
    mu, std = norm.fit(initial_u_values)
    plt.hist(initial_u_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, len(initial_u_values))
    plt.title(title)

    plt.savefig(path+"/initial_u_cool.png")
    plt.clf()


def cool_dist_v(path, initial_v_values):
    mu, std = norm.fit(initial_v_values)
    plt.hist(initial_v_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, len(initial_v_values))
    plt.title(title)

    plt.savefig(path+"/initial_v_cool.png")
    plt.clf()

def st_dist_u(path, initial_u_values):
    mu, std = norm.fit(initial_u_values)
    plt.hist(initial_u_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, len(initial_u_values))
    plt.title(title)

    plt.savefig(path+"/initial_u_st.png")
    plt.clf()


def st_dist_v(path, initial_v_values):
    mu, std = norm.fit(initial_v_values)
    plt.hist(initial_v_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, len(initial_v_values))
    plt.title(title)

    plt.savefig(path+"/initial_v_st.png")
    plt.clf()

def w_dist_u(path, initial_u_values):
    mu, std = norm.fit(initial_u_values)
    plt.hist(initial_u_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, len(initial_u_values))
    plt.title(title)

    plt.savefig(path+"/initial_u_warm.png")
    plt.clf()


def w_dist_v(path, initial_v_values):
    mu, std = norm.fit(initial_v_values)
    plt.hist(initial_v_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, len(initial_v_values))
    plt.title(title)

    plt.savefig(path+"/initial_v_warm.png")
    plt.clf()