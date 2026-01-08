import sys
import pulp

def read_input():
    for line in sys.stdin:
        for token in line.split():
            yield token

def solve():
    input_reader = read_input()

    n_equipas = int(next(input_reader))
    m_jogos = int(next(input_reader))


    pontos = {}
    games_left = {}
    for i in range(1, n_equipas + 1):
        for j in range(1, n_equipas + 1):
            if i != j:
                if i<j:
                    games_left[(i, j)] = 2



    for i in range(1, n_equipas + 1):
        pontos[i] = 0
    for i in range(1, m_jogos + 1):
        equipa_atual = int(next(input_reader))
        adversario = int(next(input_reader))
        resultado = int(next(input_reader))
        if resultado == 0:
            pontos[equipa_atual] += 1
            pontos[adversario] += 1
        elif resultado == equipa_atual:
            pontos[equipa_atual] += 3
        elif resultado == adversario:
            pontos[adversario] += 3
        if equipa_atual < adversario:
            games_left[(equipa_atual, adversario)] -= 1
        else:
            games_left[(adversario, equipa_atual)] -= 1
    
    max_pontos = int(max(pontos.values()))

    for alvo in range(1, n_equipas + 1):
        if(pontos[alvo] + 3*sum([games_left[(min(alvo, j), max(alvo, j))] for j in range(1, n_equipas + 1) if j != alvo]) < max_pontos):
            print("-1")
            continue

        prob = pulp.LpProblem("Minimizar_Vitorias", pulp.LpMinimize)

        pontos_finais = pontos.copy()

        i_wins= {}
        i_draws= {}
        for (i, j), qtd in games_left.items():
            for k in range(0, qtd):

                i_wins[(i, j, k)] = pulp.LpVariable(f"win_{i}_{j}_{k}", cat=pulp.LpBinary)
                
                i_draws[(i, j, k)] = pulp.LpVariable(f"draw_{i}_{j}_{k}", cat=pulp.LpBinary)
                
                prob += (i_wins[(i, j, k)] + i_draws[(i, j, k)] <=1)
            
            

            for k in range(0, qtd):
                pontos_finais[i] +=  3 * i_wins[(i, j, k)] + 1 * i_draws[(i, j, k)]
                pontos_finais[j] +=  3 - 3*i_wins[(i, j, k)] - 2 * i_draws[(i, j, k)]


        for t in range(1, n_equipas + 1):
            if t != alvo:
                prob += (pontos_finais[alvo] >= pontos_finais[t])

        vitorias_alvo = []
        for(i, j), qtd in games_left.items():
            for k in range(0, qtd):
                if alvo == i:
                    vitorias_alvo.append(i_wins[(i, j, k)])
                elif alvo == j:
                    vitorias_alvo.append(1 - i_wins[(i, j, k)] - i_draws[(i, j, k)])


        prob += pulp.lpSum(vitorias_alvo)


        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))

        if(not vitorias_alvo):
            print("0")
            continue
        if pulp.LpStatus[status] == 'Optimal':
            print(int(pulp.value(prob.objective)))
        else:
            print("-1")

if __name__ == "__main__":
    solve()