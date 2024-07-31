import time
import math

def lcg(seed: int) -> tuple[int, float]:
    # LCG function that produces the next seed and r (a float in range [0,1))
    # a, c, and m are arbitrary
    a: int = 423
    c: int = 532
    m: int = 623
    
    seed: int = (a * seed + c) % m
    r: float = seed / m
    
    return seed, r

def cycle_list(seed: int, size: int) -> list[float]:
    # cycle_list and randList are to create a list of random integers
    # cycle_list() will repeat lcg() size times and store each value of r in the list y
    res: list[float] = []
    for i in range(size):
        seed, r = lcg(seed)
        res.append(r)
    return res

def rand_list(seed: int, size: int, min: int, max: int) -> list[int]:
    # rand_list() seed and size are arbitrary it only affects the randomizer
    # rand_list() will use the list from cycle_list() to create a list of random in range [min,max]
    res: list[int] = []
    for i in range(size):
        rand = int(min + (max - min + 1) * cycle_list(seed, size)[i])
        res.append(rand)
    return res

def cycle(seed: int, size: int) -> float:
    # cycle and randInt are to produce a random integer in range [min,max]
    # cycle() will repeat lcg() size times
    for i in range (size):
        seed, r = lcg(seed)
    return r

# Declaring initial seed and size for ran_int
seed : int = math.floor(time.time())
size : int = math.floor(time.time()) % 1000 

def rand_int(min: int, max: int) -> int:
    # (NEW) rand_int() will have a predetermined seed and size using current time to make it more randomized
    # rand_int() produces a random integer in range [min,max] 
    rand: int
    for i in range(size):
        rand = int(min + (max - min + 1) * cycle(seed, size))
    return rand

# NOTE USAGE EXAMPLE
# The code below: 8 and 50 are arbitrary, this will produce an array with 50 elements with the elements being in the range [20,30]
# print(rand_list(8,50,20,30)) 
# The code below: 6 and 30 are arbitrary, this will produce an integer in range [10,100]
# print(rand_int(10,100)) 
    
    
    
