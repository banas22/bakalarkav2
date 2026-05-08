from logging import exception
import numpy as np
from fontTools.misc.fixedTools import floatToFixedToStr
from numpy import *
import math
from pyexpat.errors import messages

def bit_reverse(n,pocet_bitov):# obrati indexy pola do noveho pola
    # prevod z 10 na 2 sustavu
    v_2 = []
    for i in range(pocet_bitov):
        v_2.append(n%2)
        n //= 2
    ans = 0
    i = 0
    while i < len(v_2): # prevod z 2 na 10 LIFO
        ans += 2**(pocet_bitov-i-1) * v_2[i]
        i += 1
    return ans

def twiddle_factor(prvok, pocet_prvkov):
    fi = (-2*pi*prvok)/pocet_prvkov
    return cos(fi) + 1j*sin(fi)

def butterfly(butterfly_matrix, N): # funkcny
    adds, mults = 0, 0
    fazy = int(math.log2(N))
    for faza in range(1, fazy+1):
        m = 2 ** faza # pocet radixov na danu fazu
        pol = m // 2 # rozdelenie prvkov v radixe na pol
        for vzorka in range(0, N, m):
            for k in range(pol):
                w = twiddle_factor(k, m) #vypocita twiddle factor
                a = butterfly_matrix[faza-1][vzorka+k]
                b = butterfly_matrix[faza-1][vzorka+k+pol] * w
                mults += 1

                butterfly_matrix[faza][vzorka+k] = a + b
                butterfly_matrix[faza][vzorka+k+pol] = a - b
                adds += 2

    return butterfly_matrix[fazy], adds, mults

def cooley_tukey(x): # hotovy a funkcny
    adds, mults = 0, 0
    N = len(x)  # pocet prvkov je definovany dlzkou vstupneho pola
    if math.log2(N) % 1 != 0:
        raise IndexError("Neplatný počet vzoriek")
    pocet_faz = int(math.log2(N))  # pocet faz v butterfly diagrame k=log2(n)
    butterfly_matrix = np.zeros((pocet_faz + 1, N), dtype=complex)

    for i in range(N): # prevracanie indexovych bitov na vzorkach
        butterfly_matrix[0][i] = x[bit_reverse(i, pocet_faz)]

    X, adds, mults = butterfly(butterfly_matrix, N)
    return X, adds, mults

def nesudelitelne(a): # funkcny, vracia integer
    for i in reversed( range( 2, int(math.sqrt(a)+1) ) ):
        if a % i != 0:
            continue
        # tvorba nesudelitelnych cisel
        c1 = i
        c2 = a // i

        if math.gcd(c1, c2) == 1 and not (c1 == a or c2 == a):
            return int(c1)
    raise IndexError("Neplatný počet vzoriek")

def dft(x):
    adds, mults = 0, 0
    N = len(x)
    X = np.zeros(N, dtype = complex)
    k = 0
    if N == 1:
        X[0] = x[0]
        return X, 0, 0
    if N == 2:
        X[0] = x[0] + x[1]
        X[1] = x[0] - x[1]
        return X, 2, 0
    while k < N:
        n = 0
        while n < N:
            X[k] += x[n]*twiddle_factor(n*k,N)
            adds += 1
            mults += 1
            n += 1
        k +=1
    return X, adds, mults

def modInverse(a, m):
    for x in range(1, m):
        if ((a % m) * (x % m)) % m == 1:
            return x
    return 1

def prime_factor(x):
    adds, mults = 0, 0
    N = len(x)
    N1 = nesudelitelne(N)  # Ensure N1 and N2 are coprime
    N2 = N // N1
    # Good-Thomasovo mapovanie
    X_mat = np.zeros((N1, N2), dtype=complex)
    for n in range(N):
        X_mat[n % N1][n % N2] = x[n]
    # DFT riadkov a stlpcov
    for row in range(N1):
        X_mat[row, :], A, M = dft(X_mat[row, :])
        adds += A
        mults += M
    for col in range(N2):
        X_mat[:, col], A, M = dft(X_mat[:, col])
        adds += A
        mults += M

    # Vonkajsie mapovanie
    X = np.zeros(N, dtype=complex)

    # mapovanie magnitudy
    s1 = N2 * modInverse(N2, N1)
    s2 = N1 * modInverse(N1, N2)

    for k1 in range(N1):
        for k2 in range(N2):
            index = (k1 * s1 + k2 * s2) % N
            X[index] = X_mat[k1][k2]

    m_perm = (N1 + N2) % N
    m_inv = modInverse(m_perm, N)
    X = X[(m_inv * np.arange(N)) % N]
    return X, adds, mults

def split_radix(x):
    adds, mults = 0, 0
    N = len(x)
    x = np.asarray(x, dtype=complex)

    if N <= 2: # podmienka ukoncenia rekurzie
        return dft(x)

    # triedenie podla nasobku
    x_par = x[0::2]
    x_nepar_1 = x[1::4]
    x_nepar_3 = x[3::4]
    # rekurzivne volanie
    K, A_K, M_K = split_radix(x_par)
    L, A_L, M_L = split_radix(x_nepar_1)
    M, A_M, M_M = split_radix(x_nepar_3)
    adds += A_K + A_L + A_M
    mults += M_K + M_L + M_M

    X = np.zeros(N, dtype=complex) # matica pre vysledok
    polo = N // 2
    stvrt = N // 4

    for k in range(stvrt): # pocita sa butterfly diagram z dvoma cislami
        # pomocne premenne na butterfly diagram
        w1 = twiddle_factor(k, N)
        w3 = twiddle_factor(3 * k, N)
        a = L[k] * w1 + M[k] * w3
        b = 1j * (L[k] * w1 - M[k] * w3)
        # butterfly diagram 2 vzoriek
        X[k] = K[k] + a
        X[k + polo] = K[k] - a
        X[k + stvrt] = K[k + stvrt] - b
        X[k + 3 * stvrt] = K[k + stvrt] + b
        adds += 6
        mults += 4
    return X, adds, mults