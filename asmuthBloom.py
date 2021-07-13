#!/usr/bin/env python
import binascii
import mathlib
import random
import sys

class AsmuthBloom(object):
    def __init__(self, s, t, n): 
        # s = the maximal number of participants who can't get any information on the secret
        # t = threshold for uncovering the secret (shares to recombine, all shares)
        # n = number of participants
        self._t = t
        self._s = s
        self._n = n
        self.shares = None
        self._p = 0
        self._y = 0
        self._secret = 0
        
    def _find_group_for_secret(self, k):
        """Generate group Z/Zm_0 for secret, where m_0 is prime and m_0 > secret."""
        while True:
            m_0 = mathlib.get_prime(k)
            if (mathlib.primality_test(m_0)):
                return m_0

    def _check_base_condition(self, mPrimes):
        """Check if mPrimes satisfy the Asmuth-Bloom base condition.
        """
        recomb_count = self._t
        all_count = self._n
        bottom_barrier = self._s

        Mr = 1
        for i in range(1, recomb_count + 1):
            Mr = Mr * mPrimes[i]

        pMs = mPrimes[0]
        for i in range(0, bottom_barrier - 1):
            pMs = pMs * mPrimes[all_count - i + 1]

        #by definition - Mn >= Mr
        return Mr >= pMs
    
    def _get_pairwise_primes(self, k, h):
        """Generate mPrimes = n+1 primes for Asmuth-Bloom threshold scheme and secret 
        such that mPrimes_0 is k-bit prime and d_1 is h-bit prime.
        (mPrimes_1...mPrimes_n should be pairwise coprimes)
        """
        if (h < k):
            raise Exception('Not enought bits for m_1')
        all_count = self._t
        # _p is picked randomly simple number
        _p = self._find_group_for_secret(k)
        while True:
            mPrimes = [_p]
            # all_count consecutive primes starting from h-bit prime
            for prime in mathlib.get_consecutive_primes(all_count, h):
                mPrimes.append(prime)
            if (self._check_base_condition(mPrimes)):
                return mPrimes
            
    def _prod(self, coprimes):
        """Calculate pMs for maximal amount of additions and multiplications"""
        bottom_barrier = self._s
        pMs = self._p
        n = self._n
        for i in range(0, bottom_barrier - 1):
            pMs = pMs * coprimes[n - i + 1]
        return pMs
    
    def _get_modulo_base(self, secret, coprimes):
        """Calculate M' = secret + some_number * taken_prime
        that should be less that coprimes prod.
        Modulos from this number will be used as shares.
        """
        M = self._prod(coprimes)
        while True:
            A = mathlib.get_random_range(1, (M - secret) / self._p)
            y = secret + A * self._p
            if (0 <= y < M):
                break
        return y
    
    # k is m_0_bits and h is m_1_bits
    def generate_shares(self, secret, k, h):
        if (mathlib.bit_len(secret) > k):
            raise ValueError("Secret is too long")

        m = self._get_pairwise_primes(k, h)
        self._p = m.pop(0)
        
        self._y = self._get_modulo_base(secret, m)
        
        self.shares = []
        for m_i in m:
            self.shares.append((self._y % m_i, m_i))
        # shares item format: (ki, di) ki - mods, di - coprimes
        return self.shares
        
    def combine_shares(self, shares):
        y_i = [x for x, _ in shares] # remainders
        m_i = [x for _, x in shares] # coprimes
        y = mathlib.garner_algorithm(y_i, m_i)
        d = y % self._p
        return d

    def multshares(self, shares):
        shares1 = [x for x, _ in self.shares]
        shares2 = [x for x, _ in shares]
        m = [x for _, x in shares]
        self.shares = []
        for i in range(0, m.__len__):
            self.shares.append(((shares1[i]*shares2[i]) % m[i], m[i]))

    def addshares(self, shares):
        shares1 = [x for x, _ in self.shares]
        shares2 = [x for x, _ in shares]
        m = [x for _, x in shares]
        self.shares = []
        for i in range(0, m.__len__):
            self.shares.append(((shares1[i]+shares2[i]) % m[i], m[i]))

def stringToLong(s):
    return int(binascii.hexlify(s), 16)

if len(sys.argv) < 4:
    print('Usage: ./bloom.py (--random <bits> | <path>) <M> <N>')
    print(' --random <bits>     - generate random secret')
    print(' <path>              - read secret from file')
    print(' <N>                 - number of shares')
    print(' <T>                 - number of shares needed for recovery')
    print(' <S>                 - number of shares needed for recovery')
    sys.exit(1)

print("Argument List:", str(sys.argv[2]))

random = random.SystemRandom()
secret = random.getrandbits(int(sys.argv.pop(2)))

try:
    n = int(str(sys.argv[1]))
    print ('Got N = %d' % n)
except:
    print('Invalid N')

try:
    t = int(str(sys.argv[2]))
    print('Got T = %d' % t)
except:
    print('Invalid T')

try:
    s = int(str(sys.argv[3]))
    print('Got S = %d' % s)
except:
    print('Invalid S')

if t > n:
    print('N should be less or equal than M')
    sys.exit(1)

m_0_bits = 500
m_1_bits = 800

print('--------------------------------------')
print("Secret: %s" % secret)

ab = AsmuthBloom(s,t,n)

try:
    shares = ab.generate_shares(secret, m_0_bits, m_1_bits)
except ValueError as e:
    print('Cannot generate shares: ' + str(e))
    sys.exit(1)

print("Secret shares:")
for i in range(0,n):
    print ("%s: %s\n" % (i+1, shares[i]))
print('--------------------------------------')

print('Checking result')
d = ab.combine_shares(shares[0:t])
print("Recombined secret: %s" % d)
print("Test %s" % ('successful' if d == secret else 'failed'))
print('--------------------------------------')