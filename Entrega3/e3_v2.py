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
                else:
                    games_left[(j, i)] = 2



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
    

    for alvo in range(1, n_equipas + 1):

        # Cria o problema de minimização
        prob = pulp.LpProblem("Minimizar_Vitorias", pulp.LpMinimize)

        vars_jogos = {} # Para guardar referências às variáveis do PuLP

        for (i, j), qtd in games_left.items():
            if qtd > 0:
                # x_i_j: número de vezes que i ganha a j
                x_i_j = pulp.LpVariable(f"win_{i}_{j}", lowBound=0, upBound=qtd, cat=pulp.LpInteger)
                
                # x_j_i: número de vezes que j ganha a i
                x_j_i = pulp.LpVariable(f"win_{j}_{i}", lowBound=0, upBound=qtd, cat=pulp.LpInteger)
                
                # y_i_j: número de empates entre i e j
                y_i_j = pulp.LpVariable(f"draw_{i}_{j}", lowBound=0, upBound=qtd, cat=pulp.LpInteger)
                
                vars_jogos[(i, j)] = (x_i_j, x_j_i, y_i_j)
                
                # RESTRIÇÃO 1: Soma dos resultados deve ser igual aos jogos restantes
                # x_i_j + x_j_i + y_i_j == qtd
                prob += (x_i_j + x_j_i + y_i_j == qtd), f"Jogos_Restantes_{i}_{j}"

        pontos_finais = {}

        for t in range(1, n_equipas + 1):
            # Começa com os pontos já conquistados
            expressao_pontos = pontos[t]
            
            # Adiciona os pontos previstos pelas variáveis do PuLP
            for (i, j) in vars_jogos:
                x_i_j, x_j_i, y_i_j = vars_jogos[(i, j)]
                
                if t == i: 
                    # Se a equipa t é a 'i' na variável, ganha 3 pts com x_i_j e 1 com y_i_j
                    expressao_pontos += 3 * x_i_j + 1 * y_i_j
                elif t == j:
                    # Se a equipa t é a 'j' na variável, ganha 3 pts com x_j_i e 1 com y_i_j
                    expressao_pontos += 3 * x_j_i + 1 * y_i_j
                    
            pontos_finais[t] = expressao_pontos

        # RESTRIÇÃO 2: A equipa alvo tem de ter pontuação >= a todas as outras
        for t in range(1, n_equipas + 1):
            if t != alvo:
                prob += (pontos_finais[alvo] >= pontos_finais[t]), f"Vence_{t}"

        # FUNÇÃO OBJETIVO: Minimizar vitórias da equipa alvo
        # Precisamos de somar todas as variáveis de vitória onde a equipa 'alvo' ganha
        vitorias_alvo = []
        for (i, j) in vars_jogos:
            x_i_j, x_j_i, _ = vars_jogos[(i, j)]
            if alvo == i:
                vitorias_alvo.append(x_i_j)
            elif alvo == j:
                vitorias_alvo.append(x_j_i)

        prob += pulp.lpSum(vitorias_alvo), "Minimizar_Vitorias_Alvo"


        # Resolver (podes especificar o solver se necessário, e.g., GLPK, mas o default serve)
        status = prob.solve(pulp.PULP_CBC_CMD(msg=0)) # msg=0 esconde o log do solver

        # Verificar resultado
        if pulp.LpStatus[status] == 'Optimal':
            # O valor da função objetivo é o número mínimo de vitórias
            print(int(pulp.value(prob.objective)))
        else:
            # Se for 'Infeasible' (Impossível), imprime -1
            print("-1")

    

if __name__ == "__main__":
    solve()
