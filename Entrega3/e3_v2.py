import sys
from pulp import *

def input_generator():
    for line in sys.stdin:
        for token in line.split():
            yield token

def solve():
    it = input_generator()

    try:
        n = int(next(it))
        m = int(next(it))
    except StopIteration:
        return

    current_points = {i: 0 for i in range(1, n + 1)}

    games_played = {(i, j): 0 for i in range(1, n + 1) for j in range(i + 1, n + 1)}

    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))

        pair = (min(u, v), max(u, v))
        games_played[pair] += 1

        if w == 0:
            current_points[u] += 1
            current_points[v] += 1
        elif w == u:
            current_points[u] += 3
        elif w == v:
            current_points[v] += 3

    remaining_games = []
    for (i, j), cnt in games_played.items():
        if cnt < 2:
            remaining_games.append((i, j, 2 - cnt))

    for target in range(1, n + 1):
        prob = LpProblem(f"Team_{target}", LpMinimize)

        final_pts = {i: LpAffineExpression(current_points[i]) for i in range(1, n + 1)}
        target_wins = []

        for i, j, rem in remaining_games:
            if i == target:
                w_i = LpVariable(f"w_{i}_{j}_{target}", 0, rem, LpInteger)
            else:
                w_i = LpVariable(f"w_{i}_{j}_{target}", 0, rem)

            if j == target:
                w_j = LpVariable(f"l_{i}_{j}_{target}", 0, rem, LpInteger)
            else:
                w_j = LpVariable(f"l_{i}_{j}_{target}", 0, rem)

            d = LpVariable(f"d_{i}_{j}_{target}", 0, rem)


            prob += w_i + d + w_j == rem

            if i == target:
                target_wins.append(w_i)
            elif j == target:
                target_wins.append(w_j)

            final_pts[i] += 3 * w_i + d
            final_pts[j] += 3 * w_j + d

        if target_wins:
            prob += lpSum(target_wins)
        else:
            prob += 0

        for other in range(1, n + 1):
            if other != target:
                prob += final_pts[target] >= final_pts[other]

        status = prob.solve(PULP_CBC_CMD(msg=0))

        if status == LpStatusOptimal:
            print(int(value(prob.objective)))
        else:
            print(-1)

if __name__ == "__main__":
    solve()
