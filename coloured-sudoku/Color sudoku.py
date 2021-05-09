import copy
import sys


class Cell:
    def __init__(self, choices):
        self.choices = copy.deepcopy(choices)


class World:
    def __init__(self, matrix):
        self.matrix = []
        for i in matrix:
            row = []
            for j in i:
                row.append(Cell(j.choices))
            self.matrix.append(row)


def prune(choices, choice, is_nei):
    global pr
    new_choices = []
    for other in choices:
        if other[1] == choice[1]:
            continue
        if is_nei and other[0] == choice[0]:
            continue
        if is_nei and (other[1] > choice[1]) != (pr[other[0]] > pr[choice[0]]):
            continue
        new_choices.append(other)
    return new_choices


def solve(world):
    n = len(world.matrix)
    all = n * n
    for i in world.matrix:
        for j in i:
            if len(j.choices) == 1:
                all -= 1
            elif len(j.choices) == 0:
                return "DEAD END"
    if all == 0:
        for row in world.matrix:
            for cell in row:
                print(str(cell.choices[0][1]) + cell.choices[0][0], end=' ')
            print()
        sys.exit(0)

    q = 10 ** 8
    p = -(10**8)
    co = (-1, -1)
    for i in range(n):
        for j in range(n):
            c = world.matrix[i][j]
            if len(c.choices) == 1:
                continue
            deg = 0
            for k in range(n):
                if len(world.matrix[k][j].choices) > 1:
                    deg += 1
                if len(world.matrix[i][k].choices) > 1:
                    deg += 1
            deg -= 2
            if p < deg or (deg == p and 1 < len(c.choices) < q):
                p = deg
                q = len(c.choices)
                co = (i, j)
    cell = world.matrix[co[0]][co[1]]
    for i in cell.choices:
        new_world = World(world.matrix)
        for k in range(n):
            is_nei = abs(k - co[1]) == 1
            new_world.matrix[co[0]][k].choices = prune(new_world.matrix[co[0]][k].choices, i, is_nei)
            is_nei = abs(k - co[0]) == 1
            new_world.matrix[k][co[1]].choices = prune(new_world.matrix[k][co[1]].choices, i, is_nei)
        new_world.matrix[co[0]][co[1]].choices = [i]
        solve(new_world)


m, n = map(int, input().split())
all_colors = input().split()
pr = {c: p for p, c in enumerate(reversed(all_colors))}
all_numbers = [i for i in range(1, n+1)]
matrix = []
for i in range(n):
    row = []
    for j in input().split():
        colors = set(all_colors)
        numbers = set(all_numbers)
        if j[0].isdigit():
            numbers = {int(j[0])}
        if j[1] != '#':
            colors = {j[1]}
        choices = []
        for c in colors:
            for num in numbers:
                choices.append((c, num))
        row.append(Cell(choices))
    matrix.append(row)
world = World(matrix)
solve(world)
