import copy
from collections import defaultdict


class State():
    def __init__(self, positions, action):
        self.positions = positions
        self.action = action

    def __key(self):
        return str(self.positions)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, State):
            return self.__key() == other.__key()
        return NotImplemented

    def do_action(self, action):  # action = (from,to) move the last card from .. to ..
        if self.positions[action[0]][0] == "#":
            return 0
        else:
            if self.positions[action[1]][0] == "#":
                self.positions[action[1]].pop()
                self.positions[action[1]].append(self.positions[action[0]][-1])
                self.positions[action[0]].pop()
                if len(self.positions[action[0]]) == 0:
                    self.positions[action[0]].append("#")
                #print(action)
                # for a in self.positions:
                #    print(a)
                return self.positions
            else:
                if int(self.positions[action[1]][-1][:-1]) > int(self.positions[action[0]][-1][:-1]):
                    self.positions[action[1]].append(self.positions[action[0]][-1])
                    self.positions[action[0]].pop()
                    if len(self.positions[action[0]]) == 0:
                        self.positions[action[0]].append("#")
                    #print(action)
                    # for a in self.positions:
                    #    print(a)
                    return self.positions
                else:
                    return 0


class Problem():
    def __init__(self, initial_state, actions, m, n):
        self.initial_state = initial_state
        self.actions = actions
        self.m = m
        self.n = n

    def goal_test(self, state):
        flag = 0
        for k in state.positions:
            letters = []
            numbers = []
            for i in range(len(k)):
                if k[i][0] != "#":
                    letters.append(k[i][-1])
                    numbers.append(k[i][:-1])
            numbers = list(map(int, numbers))
            if len(letters) > 0:
                if all(numbers[p] >= numbers[p + 1] for p in range(len(numbers) - 1)) and all(
                        elem == letters[0] for elem in letters):
                    flag += 1
            else:
                flag += 1

        if flag == len(state.positions):
            return True
        return False

    def h(self, state):
        # number of unsorted elements of the same color in each list +
        # number of elements not in the list with the maximum number of elements of that color
        if self.goal_test(state):
            return 0
        else:
            h = 0
            for s in state.positions:
                colors = set()
                clr = list()
                c_dict = {}
                for l in range(len(s)):
                    if s[l][0] != "#":
                        colors.add(s[l][-1])
                        clr.append(s[l][-1])
                    for c in colors:
                        val = list()
                        if s[l][-1] == c:
                            val.append(s[l][:-1])
                        c_dict[c] = val
                for key, value in c_dict.items():
                    a = value
                    value.sort(reverse=True)
                    for j in value:
                        h += abs(value.index(j) - a.index(j))
                for q in clr:
                    if q != clr[0]:
                        h += 1
            return h


def Solution(cameFrom, state):
    sol = list()
    depth = 0
    sol.append(state)
    while state in cameFrom.keys():
        state = cameFrom[state]
        sol.append(state)
    print("solution was found in depth " + str(len(sol) - 1))
    for s in sol[::-1]:
        print("depth: " + str(depth))
        print(s.action)
        for p in s.positions:
            print(str(p))
        depth += 1
    return sol[::-1]


def create_neighbors(problem, state):
    global nc
    neighbors = []
    for action in problem.actions:
        neighbor = State(copy.deepcopy(state.positions), action)
        neighbor.positions = neighbor.do_action(action)
        neighbor.action = action
        if neighbor.positions != 0:
            neighbors.append(neighbor)
            nc += 1
    return neighbors


def A_star(problem):
    global nc
    global ne
    open_list = list()
    open_list.append(problem.initial_state)
    came_from = dict()

    g = defaultdict(lambda: float('inf'))
    g[problem.initial_state] = 0

    f = defaultdict(lambda: float('inf'))
    f[problem.initial_state] = problem.h(problem.initial_state)

    while len(open_list) > 0:
        tmp = dict()
        for a in open_list:
            if a in f.keys():
                tmp[a] = f[a]
        temp = min(tmp.values())
        for key, value in tmp.items():
            if temp == value:
                curr = key
        if problem.goal_test(curr):
            print("nodes created: " + str(nc))
            print("nodes explored: " + str(ne))
            return Solution(came_from, curr)
        open_list.remove(curr)
        ne += 1
        neighbors = create_neighbors(problem, curr)
        for n in neighbors:
            tentative_g = g[curr] + 1
            if tentative_g < g[n]:
                came_from[n] = curr
                g[n] = tentative_g
                f[n] = g[n] + problem.h(n)
                if n not in open_list:
                    open_list.append(n)
    print("failure")
    return -1


# main
k, m, n = map(int, input().split())
initial = []
actions = []
for i in range(k):
    initial.append(list(map(str, input().split())))
for j in range(k):
    for h in range(j + 1, k):
        actions.append((j, h))
        actions.append((h, j))
initial_state = State(initial, None)
nc = 1
ne = 1
this_problem = Problem(initial_state, actions, m, n)
A_star(this_problem)
