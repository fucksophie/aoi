
def totalXpToLevel(n):
    return 5*(n**2)+50*n+100

def levelToXp(n):
    return int(5/6*n*(2*n*n+27*n+91))

def xpToLevel(xp):
    remaining_xp = int(xp)
    level = 0

    while remaining_xp >= totalXpToLevel(level):
        remaining_xp -= totalXpToLevel(level)
        level += 1

    return level
