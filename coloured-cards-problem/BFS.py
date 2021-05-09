import queue
import copy


class State():
    def __init__(self, positions, parent, action):
        self.positions = positions
        self.action = action
        self.parent = parent

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
                #   print(a)
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
    child = State(copy.deepcopy(parent.positions), parent, parent.action)
    child.action = action
    child.positions = child.do_action(action)
    child.parent = parent
    return child


def solution(problem, state):
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


def BFS(problem):
    node = problem.initial_state
    if problem.goal_test(node.positions):
        print("this is a goal node, no action taken: ")
        print(node.positions)
        return 0
    frontier = queue.Queue()
    frontier.put(node)
    seen = list()
    seen.append(node.positions)
    explored = []
    while True:
        if frontier.empty():
            print("failure")
            return False
        node = frontier.get()
        explored.append(node.positions)
        for action in problem.actions:
            child = child_node(node, action)
            if child.positions == 0:
                continue
            if child.positions not in explored or child.positions not in seen:
                if problem.goal_test(child.positions):
                    print("solution path: ")
                    solution(problem, child)
                    print("nodes created: " + str(frontier.qsize()))
                    print("nodes explored: " + str(len(explored)))
                    return 0
                frontier.put(child)
                seen.append(child.positions)


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
initial_state = State(initial, 0, None)
this_problem = Problem(initial_state, actions, m, n)
BFS(this_problem)
