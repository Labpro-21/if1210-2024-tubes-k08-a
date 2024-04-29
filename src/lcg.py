# LCG function that produces the next seed and r (a float in range [0,1))
def lcg(seed: int) -> tuple[int, float]:
    # a, c, and m are arbitrary
    a: int = 423
    c: int = 532
    m: int = 623
    
    seed: int = (a * seed + c) % m
    r: float = seed / m
    
    return seed, r

# cycleList and randList are to create a list of random integers
# cycleList() will repeat lcg() size times and store each value of r in the list y
def cycleList(seed: int, size: int) -> list[float]:
    y: list[float] = []
    for i in range(size):
        seed, r = lcg(seed)
        y.append(r)
    return y

# randList() seed and size are arbitrary it only affects the randomizer
# randList() will use the list from cycleList to create a list of random in range [min,max]
def randList(seed: int, size: int, min: int, max: int) -> list[int]:
    z: list[int] = []
    for i in range(size):
        rand = int(min + (max - min + 1) * cycleList(seed, size)[i])
        z.append(rand)
    return z

# cycle and randInt are to produce a random integer in range [min,max]
# cycle() will repeat lcg() size times
def cycle(seed: int, size: int) -> float:
    for i in range (size):
        seed, r = lcg(seed)
    return r

# randInt() seed and size are arbitrary it only affects the randomizer
# randInt() produces a random integer in range [min,max] 
def randInt(seed: int, size: int, min: int, max: int) -> int:
    rand: int
    for i in range(size):
        rand = int(min + (max - min + 1) * cycle(seed, size))
    return rand

# NOTE USAGE EXAMPLE
# The code below: 8 and 50 are arbitrary, this will produce an array with 50 elements with the elements being in the range [20,30]
print(randList(8,50,20,30)) 
# The code below: 6 and 30 are arbitrary, this will produce an integer in range [10,100]
# print(randInt(6,30,10,100)) 
    
    
    
