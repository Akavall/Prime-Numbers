# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 20:07:18 2012

@author: Kirill Temlyakov
"""

from math import sqrt
from itertools import chain

class WrongTypeError(Exception):
    pass

class NegativeIntegerError(Exception):
    pass

class LowerGreaterThanUpperError(Exception):
    pass

def get_pairs(n, gap):
    '''
    Return a list of pairs, is a "step" between 0 and n.
    
    Input Type: 
        
        n : integer
        
        gap : integer
        
    Output Type:
        
        List of tuples
    
    For example:
        
    >>> get_pairs(25, 10)
    [(0, 10), (10, 20), (20, 25)]
    >>> get_pairs(40, 10)
    [(0, 10), (10, 20), (20, 30), (30, 40)]
    '''
    lower_bounds = xrange(0, n, gap)
    upper_bounds = xrange(gap, n, gap)
    
    pairs = zip(lower_bounds, upper_bounds)
    
    pairs.append((lower_bounds[-1], n))
    return pairs
    
def check_input(x):
    if isinstance(x, int) == False:
        raise WrongTypeError('Input should be a positive integer')
    if x < 0:
        raise NegativeIntegerError('Integer should not be negative')
    

class Primes(object):
    '''
    isprime(n) checks if n is prime
    
    sieve(n) returns a generator of all primes from 2 to n(not including)
    
    primes_in_range(lower, upper) returns a generator of all primes between
    lower(including) and upper(not including)
                                  
    primes_list(n) returns a generator of all primes from 2 to n(not including)
    this method is more space efficient and can handle larger n's than sieve.
    
    twin_numbers(n) returns a generataor of all twin prime pairs up to
    n(not including)
    '''
    def isprime(self, x):
        '''
        Returns a boolean value, true if input integer is prime
        and false if input integer is not prime.
        
        Input Type : x is a non-negative integer
        
        Output Type : boolean
        
        >>> Primes().isprime(0)
        False
        >>> Primes().isprime(1)
        False
        >>> Primes().isprime(2)
        True
        >>> Primes().isprime(23)
        True
        >>> Primes().isprime(3748)
        False
        '''
        check_input(x)
            
        if x in (0,1):
            return False
        elif x == 2: return True
        elif x%2 == 0: return False
        else:
            for i in xrange(3,int(sqrt(x))+2,2):
                if x%i == 0:
                    return False
                    break
        return True
    def sieve(self, n):
        ''' 
        Returns all primes in the range from 2 to n
        where n is not included. 
        
        Input Type: non-negative integer
        
        Output Type: generator of positive integers (primes)
        that are sorted in increasing order
        
        >>> list(Primes().sieve(10))
        [2, 3, 5, 7]
        >>> list(Primes().sieve(50))
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        >>> len(list(Primes().sieve(50000)))
        5133
        >>> len(list(Primes().sieve(500000)))
        41538
        '''        
        check_input(n)
        numbers = range(n)
        numbers[1] = 0
        prime = 2 # this is only to keep the while loop
                  # condition happy
        first_primes = []
        
        while prime < n**0.5:
            for ele in numbers:
                if ele != 0:
                    prime = ele
                    break
            
            first_primes.append(prime)
                
            for i in xrange(0, n, prime):
                numbers[i] = 0
                
        second_primes = [ele for ele in numbers if ele]
        
        for ele in first_primes:
            yield ele
        for ele in second_primes:
            yield ele
        
    def primes_in_range(self, lower, upper):
        '''
        Returns a generator of primes in a range between 
        upper lower and upper values. Where lower values is included
        while upper value is not included.
        
        Input Type:
            
            lower : positive integer (not greater than upper)
            
            upper : positibe integer (not less than lower)
        
        >>> list(Primes().primes_in_range(3, 29))
        [3, 5, 7, 11, 13, 17, 19, 23]
        >>> list(Primes().primes_in_range(144, 289))
        [149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283]
        '''
        check_input(lower)
        check_input(upper)
        if lower > upper:
            raise LowerGreaterThanUpperError('lower bound cannot be greater than upper bound')
                
        numbers = range(lower, upper)
        n = len(numbers)
        key_num = upper ** 0.5
        
        primes = self.sieve(int(key_num) + 1)
        
        if lower > upper ** 0.5:
            for prime in primes:
                remainder = prime - lower % prime
                if lower % prime == 0:
                    remainder = 0
                for i in xrange(remainder, n, prime):
                    numbers[i] = 0
            for num in numbers:
                if num:
                    yield num
        else:
            small_primes = []
            for prime in primes:
                if prime > key_num:
                    break
                if prime >= lower:
                    small_primes.append(prime)
                    
            #small_primes + self.primes_in_range(int(key_num) + 1, upper)
            
            
            for ele in small_primes:
                yield ele
            for ele in self.primes_in_range(int(key_num) + 1, upper):
                yield ele
                
            
    def primes_list(self, n):
        # This is a pretty space efficient sieve. For example range(200 * 10 ** 6)
        # causes memory error on most sytems; this method avoids this problem, by
        # splitting the range in segments of 10 * 10 ** 6.
        '''
        Returns a generator of prime numbers between 2 and n, where n is no included.
        
        Input Type : non-negative integer
        
        Output Type : generator of integers (primes) that are sorted in increasing order
        
        >>> list(Primes().primes_list(25))
        [2, 3, 5, 7, 11, 13, 17, 19, 23]
        >>> list(Primes().primes_list(100))
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        >>> len(list(Primes().primes_list(50 * 10 ** 6)))
        3001134
        >>> len(list(Primes().primes_list(200 * 10 ** 6)))
        11078937
        '''
 
        check_input(n)
        if n < 10000000:
            return self.sieve(n)
        else:
            pairs = get_pairs(n, 10000000)[1:]
            
            primes_list = self.primes_in_range(2, 10000000)
            
            for pair in pairs:
                primes_list = chain(primes_list, self.primes_in_range(*pair))
        return primes_list
    def twin_primes(self, n):
        '''
        Return generator that contains twin prime numbers. Each element of 
        a generator is a tuple.
        
        Input Type : non-negative integer
        
        Output Type: generator that contains pairs of twin numbers, each pair
                     is a tuple
        >>> list(Primes().twin_primes(30))
        [(3, 5), (5, 7), (11, 13), (17, 19)]
        >>> list(Primes().twin_primes(100))
        [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73)]
        >>> len(list(Primes().twin_primes(10000)))
        205
        >>> len(list(Primes().twin_primes(20 * 10 ** 6)))
        107407
        '''
        primes_list = self.primes_list(n)
        prev = -1 # just an arbitrary number to start of prev (just can't use 0)
        for ele in primes_list:
            if prev + 2 == ele:
                yield (prev, ele)
            prev = ele
        
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose = True)
    