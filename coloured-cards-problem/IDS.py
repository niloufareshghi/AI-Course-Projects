import copy


class State():
    def __init__(self, positions, parent, action):
        self.parent = parent
        self.positions = positions
        self.action = action

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
                # print(action)
                # for a in self.positions:
                #    print(a)
                return self.positions
            else:
                if int(self.positions[action[1]][-1][:-1]) > int(self.positions[action[0]][-1][:-1]):
                    self.positions[action[1]].append(self.positions[action[0]][-1])
                    self.positions[action[0]].pop()
                    if len(self.positions[action[0]]) == 0:
                        self.positions[action[0]].append("#")
                    # print(action)
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
        for k in state:
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

        if flag == len(state):
            return True
        return False


def child_node(parent, action):
    global nc
    child = State(copy.deepcopy(parent.positions), parent, parent.action)
    child.action = action
    child.positions = child.do_action(action)
    if child.positions != 0:
        nc += 1
    child.parent = parent
    return child


def Solution(problem, state):
    sol = list()
    depth = 0
    sol.append(state)
    while state.positions != problem.initial_state.positions:
        sol.append(state.parent)
        state = state.parent
    print("answer was found in depth " + str(len(sol) - 1))
    for s in sol[::-1]:
        print("depth: " + str(depth))
        print(s.action)
        for p in s.positions:
            print(str(p))
        depth += 1
    return sol[::-1]


def Recursive_DLS(node, problem, limit):
    global nc
    global ne
    if problem.goal_test(node.positions):
        print("nodes created: " + str(nc))
        print("nodes explored: " + str(ne))
        print("solution path: ")
        return Solution(problem, node)
    else:
        if limit == 0:
            print("cutoff")
            return "cutoff"
        else:
            cutoff_occured = False
            ne += 1
            for action in problem.actions:
                child = child_node(node, action)
                if child.positions == 0:
                    continue
                result = Recursive_DLS(child, problem, limit - 1)
                if result == "cutoff":
                    cutoff_occured = True
                else:
                    if result != "cutoff":
                        return result
            if cutoff_occured:
                print("cutoff")
                return "cutoff"
            else:
                print("fail")
                return -1


def DLS(problem, limit):
    node = problem.initial_state
    return Recursive_DLS(node, problem, limit)


def IDS(problem):
    depth = 0
    while depth > -1:
        result = DLS(problem, depth)
        depth += 1
        if result != "cutoff":
            return result


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
initial_state = State(initial, None, None)
nc = 1
ne = 1
this_problem = Problem(initial_state, actions, m, n)
IDS(this_problem)
