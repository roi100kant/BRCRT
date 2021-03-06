#!/usr/bin/env python
import binascii
import mathlib
import random

class AsmuthBloom(object):
    def __init__(self, n, t, s, opM):
        # s = the maximal number of participants who can't get any information on the secret
        # t = threshold for uncovering the secret (shares to recombine, all shares)
        # n = number of participants
        self._n = n
        self._t = t
        self._s = s
        self.coprimes = None
        # self._bound = 0         # a prime number all secrets are lower than
        self._p = 0             # a prime number bigger than bound^(n/s)
        self._M = opM

    def _find_group_for_secret(self, k):
        """Generate group Z/Zm_0 for secret, where m_0 is prime and m_0 > secret."""
        while True:
            m_0 = mathlib.get_prime(k)
            if (mathlib.primality_test(m_0)):
                return m_0

    # mPrimes[0] = p
    def _check_base_condition(self, mPrimes):
        """Check if mPrimes satisfy the Asmuth-Bloom base condition.
        """
        t = self._t
        n = self._n

        Mr = 1
        for i in range(1, t + 2):
            Mr = Mr * mPrimes[i]

        last_t_primes = mPrimes[0]
        for i in range(1, t + 1):
            last_t_primes *= mPrimes[n - i + 1]

        #by definition - Mn >= Mr
        return Mr >= last_t_primes

    def _get_pairwise_primes(self, k, h):
        """Generate mPrimes = n+1 primes for Asmuth-Bloom threshold scheme and secret 
        such that mPrimes_0 is k-bit prime and d_1 is h-bit prime.
        (mPrimes_1...mPrimes_n should be pairwise coprimes)
        """
        if (h < k):
            raise Exception('Not enought bits for m_1')
        n = self._n

        # _p is picked randomly big enough to support the multiplications
        # self._bound = self._find_group_for_secret(k + 1)
        # big_p_bit_len = int(k*(n // self._s))
        _p = self._find_group_for_secret(k)

        while True:
            mPrimes = [_p]
            # n consecutive primes starting from h-bit prime
            for prime in mathlib.get_consecutive_primes(n, h):
                mPrimes.append(prime)
            if (self._check_base_condition(mPrimes)):
                return mPrimes

    # coPrimes[0] != p (we popped p before), coprimes = [m_1, ... ,m_n]
    def _prod(self, coprimes):
        """Calculate pMs for maximal amount of additions and multiplications"""
        s = int(self._s)
        n = int(self._n)

        pMs = self._p
        for i in range(1, s): # from 1 to s-1
            pMs = pMs * coprimes[n - i]
        if(self._M == 0):
            t = self._t
            Mr = 1
            for i in range(0, t + 1): # from 0 to t
                Mr = Mr * coprimes[i]
            return random.randint(pMs,Mr)
        else:
            return pMs

    # coPrimes[0] != p (we popped p before), coprimes = [m_1, ... ,Mn]
    def _get_modulo_base(self, secret, coprimes):
        """Calculate y = secret + some_number * taken_prime
        that should be less that coprimes prod.
        Modulos from this number will be used as shares.
        """
        M = self._prod(coprimes)
        while True:
            A = random.randint(1, (M - secret) // self._p)
            y = secret + A * self._p
            if (0 <= y < M):
                break
        return y

    # k is m_0_bits and h is m_1_bits
    def _generate_coPrimes(self, k, h):
        self.coprimes = self._get_pairwise_primes(k, h)
        self._p = self.coprimes.pop(0)

    def generate_shares(self, secret, k, h):
        if (mathlib.bit_len(secret) > k):
            raise ValueError("Secret is too long")

        if(self.coprimes == None):
            self._generate_coPrimes(k, h)

        m = self.coprimes
        y = self._get_modulo_base(secret, m)

        shares = []
        for m_i in m:
            shares.append((y % m_i, m_i))
        # shares item format: (ki, di) ki - mods, di - coprimes
        return shares

    def combine_shares(self, shares):
        y_i = [x for x, _ in shares] # remainders
        m_i = [x for _, x in shares] # coprimes
        y = mathlib.garner_algorithm(y_i, m_i)
        d = y % self._p
        return d

    def multshares(self, shares1, shares2):
        moduli1 = [x for x, _ in shares1]
        moduli2 = [x for x, _ in shares2]
        m = self.coprimes
        mul_shares = []
        for i in range(0, len(m)):
            mul_shares.append(((moduli1[i]*moduli2[i]) % m[i], m[i]))
        return mul_shares

    def addshares(self, shares1, shares2):
        moduli1 = [x for x, _ in shares1]
        moduli2 = [x for x, _ in shares2]
        m = self.coprimes
        add_shares = []
        for i in range(0, len(m)):
            add_shares.append(((moduli1[i] + moduli2[i]) % m[i], m[i]))
        return add_shares

def stringToLong(s):
    return int(binascii.hexlify(s), 16)