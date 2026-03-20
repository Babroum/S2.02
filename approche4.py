nodes = {}

def placer(x, y, joueur, n=5):
    nodes[(x, y)] = joueur

    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dx, dy in directions:
        voisin = (x + dx, y + dy)
        if voisin in nodes:
            pass

    return verifier_victoire(x, y, joueur, n)

def compter_direction(x, y, joueur, dx, dy):
    compte = 0
    cx, cy = x + dx, y + dy
    while (cx, cy) in nodes and nodes[(cx, cy)] == joueur:
        compte += 1
        cx += dx
        cy += dy
    return compte

def verifier_victoire(x, y, joueur, n):
    directions = [(1,0),(0,1),(1,1),(1,-1)]
    for dx, dy in directions:
        total = 1
        total += compter_direction(x, y, joueur, dx, dy)
        total += compter_direction(x, y, joueur, -dx, -dy)
        if total >= n:
            return True
    return False

def reinitialiser():
    nodes.clear()
