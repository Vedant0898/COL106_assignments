import random
import math


# To generate random prime less than N
def randPrime(N):
    primes = []
    for q in range(2, N+1):
        if (isPrime(q)):
            primes.append(q)
    return primes[random.randint(0, len(primes)-1)]


# To check if a number is prime
def isPrime(q):
    if (q > 1):
        for i in range(2, int(math.sqrt(q)) + 1):
            if (q % i == 0):
                return False
        return True
    else:
        return False


# pattern matching
def randPatternMatch(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatch(q, p, x)


# pattern matching with wildcard
def randPatternMatchWildcard(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatchWildcard(q, p, x)


# return appropriate N that satisfies the error bounds
def findN(eps, m):
    # ---------------------------------------------------------------------------
    # | INPUT                                                                   |
    # | eps : error bound                                                       |
    # | m : length of pattern                                                   |
    # |                                                                         |
    # | OUTPUT                                                                  |
    # | N : upper bound for random prime                                        |
    # |                                                                         |
    # | Time Complexity  : O(1)                                                 |
    # | Space Complexity : O(log(m/eps))                                        |
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    # | Proof of correctness of findN                                           |
    # |                                                                         |
    # | Let a hash value of pattern                                             |
    # | Let b hash value of substring of document of length                     |
    # | Therefore false positive occurs when a != b , but a mod q == b mod q    |
    # | Thus, q | (a - b)                                                       |
    # |                                                                         |
    # | a-b is a m bit number in base 26                                        |
    # | Hence, (a - b) = sum_{i=0}^{m-1} (a[i] - b[i]) * 26^i                   |
    # | (a - b) <= sum_{i=0}^{m-1} (26) * 26^i = 26^m                           |
    # |                                                                         |
    # | Number of prime divisors of a-b  = log2(a-b)  <= log2(26^m)             |
    # | Thus false positive occurs when q is one of these prime divisors ,      |
    # | which are at most m*log2(26)                                            |
    # | Thus probability of false positive is at most m*log2(26)/pi(N)          |
    # |                                                                         |
    # | m*log2(26)/pi(N) <= eps      =>       pi(N) >= m*log2(26)/eps           |
    # | We have been given that pi(N) >= N / (2 * log2(N))                      |
    # | N / (2 * log2(N)) >= m*log2(26)/eps                                     |
    # |                                                                         |
    # | Consider first approxmation of N = 2 * m * log2(26) / eps               |
    # | Now the next approximation is N = N * log2(N) * 10                      |
    # | The multiplication by 10 ensures that N satisfies the above inequality  |
    # | In the end we return int(N) + 1                                         |
    # ---------------------------------------------------------------------------

    a = 10
    N = 2 * math.log2(26) * m / eps
    N = N * math.log2(N) * a

    return int(N) + 1


# Return sorted list of starting indices where p matches x
def modPatternMatch(q, p, x):
    m = len(p)
    # Compute the hash of pattern and pre-compute the value of (26^(m-1) % q) and store it in pre_comp
    pat_hash, pre_comp = hash(p, 0, m, q)

    # Compute the hash of first m characters of document
    prev_hash, _ = hash(x, 0, m, q)
    occurence_lst = []                  # Initialize list for storing indexes
    if prev_hash == pat_hash:           # check for index 0
        occurence_lst.append(0)

    for i in range(1, len(x)-m+1):
        # Calculate new hash for document for characters from i to i+m-1
        new_hash = rehash(x[i+m-1], x[i-1], q, prev_hash, pre_comp)  # rehash
        if new_hash == pat_hash:
            occurence_lst.append(i)     # append to list if hash is equal
        prev_hash = new_hash            # store the new hash in prev_hash

    return occurence_lst                # return list of indexes


# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q, p, x):
    m = len(p)
    # Compute the hash of pattern, position of question mark and pre-compute the
    # value of (26^(m-1) % q), (26^(m-pos-1) % q) then store it in pre_comp1 and pre_comp2
    pat_hash, q_pos, pre_comp1, pre_comp2 = wildcard_pat_hash(p, 0, m, q)

    # Compute the hash of first m characters of document
    prev_hash = wildcard_string_hash(x, 0, m, q, q_pos)
    occurence_lst = []                  # Initialize list for storing indexes
    if prev_hash == pat_hash:           # check for index 0
        occurence_lst.append(0)

    for i in range(1, len(x)-m+1):
        # Calculate new hash for document for characters i to i+m-1
        new_hash = wildcard_string_rehash(
            prev_hash, x[i+m-1], x[i-1], x[i+q_pos-1], x[i+q_pos], pre_comp1, pre_comp2, q)
        if new_hash == pat_hash:
            occurence_lst.append(i)     # append to list if hash is equal
        prev_hash = new_hash            # store the new hash in prev_hash

    return occurence_lst                # return list of indexes


def identifier(c):
    # ---------------------------------------------------------------------------
    # | INPUT                                                                   |
    # | c : char (A-Z and ?)                                                    |
    # |                                                                         |
    # | OUTPUT                                                                  |
    # | int : -1 for '?' and 0-25 for A-Z                                       |
    # |                                                                         |
    # | Time Complexity  : O(1)                                                 |
    # | Space Complexity : O(1)                                                 |
    # ---------------------------------------------------------------------------
    if c == "?":
        return -1

    return ord(c) - ord('A')


def hash(s, low, high, q):
    # ---------------------------------------------------------------------------
    # | INPUT                                                                   |
    # | s : document string                                                     |
    # | low, high : end points of string which is to be hashed                  |
    # | q : prime number                                                        |
    # |                                                                         |
    # | OUTPUT                                                                  |
    # | int : hash value of s[low:high]                                         |
    # |                                                                         |
    # | Time Complexity  : O(m)                                                 |
    # | Space Complexity : O(log(q))                                            |
    # ---------------------------------------------------------------------------
    val = 0
    pre_comp = 1
    for i in range(low, high):
        c = s[i]
        val = ((val * 26) % q + identifier(c)) % q
        if i == high-1:
            break
        pre_comp = (pre_comp * 26) % q

    return val, pre_comp


def rehash(new_char, old_char, q, prev_hash, pre_comp):
    # ---------------------------------------------------------------------------
    # | INPUT                                                                   |
    # | new_char : new character to be added to the hash                        |
    # | old_char : old character to be removed from the hash                    |
    # | q : prime number                                                        |
    # | prev_hash : previous hash value                                         |
    # | pre_comp : precomputed value of 26^(m-1) % q                            |
    # |                                                                         |
    # | OUTPUT                                                                  |
    # | int : new hash value                                                    |
    # |                                                                         |
    # | Time Complexity  : O(1)                                                 |
    # | Space Complexity : O(log(q))                                            |
    # ---------------------------------------------------------------------------
    new_hash = (((prev_hash - (identifier(old_char) * pre_comp) % q) * 26) %
                q + identifier(new_char)) % q
    return new_hash


def wildcard_pat_hash(s, low, high, q):
    # ---------------------------------------------------------------------------
    # | INPUT                                                                   |
    # | s : document string                                                     |
    # | low, high : end points of string which is to be hashed                  |
    # | q : prime number                                                        |
    # |                                                                         |
    # | OUTPUT                                                                  |
    # | val       - int : hash value of s[low:high]                             |
    # | q_pos     - int : position of question mark (pos)                       |
    # | pre_comp1 - int : precomputed value of (26^(m-1)) % q                   |
    # | pre_comp2 - int : precomputed value of (26^(m-pos-1)) % q               |
    # |                                                                         |
    # | Time Complexity  : O(m)                                                 |
    # | Space Complexity : O(log(q))                                            |
    # ---------------------------------------------------------------------------
    q_pos = -1
    val = 0
    pre_comp1 = 1                                       # 26^(m-1) mod q
    pre_comp2 = 1                                       # 26^(m-pos-1) mod q
    for i in range(low, high):
        c = s[i]
        if q_pos >= 0:
            pre_comp2 = (pre_comp2 * 26) % q
        if identifier(c) == -1:
            q_pos = i
        if i != q_pos:
            val = ((val * 26) % q + identifier(c)) % q
        else:
            val = (val * 26) % q

        if i == high-1:
            break
        pre_comp1 = (pre_comp1 * 26) % q

    return val, q_pos, pre_comp1, pre_comp2


def wildcard_string_hash(s, low, high, q, q_pos):
    # ---------------------------------------------------------------------------
    # | INPUT                                                                   |
    # | s : document string                                                     |
    # | low, high : end points of string which is to be hashed                  |
    # | q : prime number                                                        |
    # | q_pos : position of question mark                                       |
    # |                                                                         |
    # | OUTPUT                                                                  |
    # | val - int : hash value of s[low:high] - s[q_pos]                        |
    # |                                                                         |
    # | Time Complexity  : O(m)                                                 |
    # | Space Complexity : O(log(q))                                            |
    # ---------------------------------------------------------------------------

    val = 0
    for i in range(low, high):
        c = s[i]

        if i != q_pos:
            val = ((val * 26) % q + identifier(c)) % q
        else:
            val = (val * 26) % q

    return val


def wildcard_string_rehash(prev_hash, new_char, old_char, old_q_char, new_q_char, pre_comp1, pre_comp2, q):
    # ---------------------------------------------------------------------------
    # | INPUT                                                                   |
    # | prev_hash : previous hash value                                         |
    # | new_char : new character to be added to the hash                        |
    # | old_char : old character to be removed from the hash                    |
    # | old_q_char : old question mark character to be removed from the hash    |
    # | new_q_char : new question mark character to be added to the hash        |
    # | q : prime number                                                        |
    # | pre_comp1 : precomputed value of 26^(m-1) % q                           |
    # | pre_comp2 : precomputed value of 26^(m-pos-1) % q                       |
    # |                                                                         |
    # | OUTPUT                                                                  |
    # | int : new hash value                                                    |
    # |                                                                         |
    # | Time Complexity  : O(1)                                                 |
    # | Space Complexity : O(log(q))                                            |
    # ---------------------------------------------------------------------------
    new_hash = ((((prev_hash - (identifier(old_char) * pre_comp1) % q) + (identifier(old_q_char)
                * pre_comp2) % q) * 26) + identifier(new_char) - (identifier(new_q_char) * pre_comp2) % q) % q

    return new_hash


# if __name__ == "__main__":

#     q = 101
#     pat = "AS?A"
#     s = "NASWASUGPNDNBFJKSDHNFJKDSHNFJDSHNFJSDANFJKSDNAKJNSADKJASKDNMANKDASNDASJDNJSAFDSLKFSDLJARIOJDFIHSFUHASDFUHAIFHJAIHJGFAHGAJFGAOSIFDOEIFRIEURIEWRFUGEHUFGDVFBJVBNCVIKDJSFIASJEOEIKJSDJDFKGDKFGASFA"
#     lst = modPatternMatchWildcard(101, pat, s)
#     print(lst)
