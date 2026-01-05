import sys
from pulp import *

def solve():
    # 1. Leitura Robusta do Input
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator)) # Número de equipas
        m = int(next(iterator)) # Jogos já realizados
    except StopIteration:
        return

    # 2. Inicializar Estruturas de Dados
    # Pontos atuais de cada equipa
    current_points = {i: 0 for i in range(1, n + 1)}
    
    # Matriz para contar jogos realizados entre par (u, v)
    # Usamos chaves ordenadas (menor, maior) para evitar duplicatas (1,2) e (2,1)
    games_played_count = {}
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            games_played_count[(i, j)] = 0

    # 3. Processar os 'm' jogos já realizados
    for _ in range(m):
        try:
            u = int(next(iterator))
            v = int(next(iterator))
            w = int(next(iterator)) # Vencedor: 0=Empate, u=u venceu, v=v venceu
        except StopIteration:
            break

        # Normalizar par (menor, maior)
        if u < v:
            pair = (u, v)
        else:
            pair = (v, u)

        if pair in games_played_count:
            games_played_count[pair] += 1

        # Atribuir Pontos
        if w == 0:  # Empate
            current_points[u] += 1
            current_points[v] += 1
        elif w == u: # u venceu
            current_points[u] += 3
        elif w == v: # v venceu
            current_points[v] += 3

    # 4. Identificar Jogos Restantes
    # Assume campeonato a duas voltas (2 jogos entre cada par)
    remaining_games = []
    for (i, j), count in games_played_count.items():
        rem = 2 - count
        if rem > 0:
            remaining_games.append((i, j, rem))

    # 5. Resolver PL para cada equipa
    for target_team in range(1, n + 1):
        # Criar o Problema de Minimização
        prob = LpProblem(f"Team_{target_team}_Analysis", LpMinimize)

        # Variáveis para guardar vitórias da equipa alvo (para o objetivo)
        target_wins_vars = []

        # Dicionário para guardar as expressões de pontos finais
        # Começamos com os pontos atuais (constante)
        final_points_expr = {t: current_points[t] for t in range(1, n + 1)}

        # --- Definir Variáveis para Jogos Restantes ---
        for (i, j, rem) in remaining_games:
            # Variáveis inteiras >= 0
            # w_i: vitórias de i contra j
            # d:   empates
            # w_j: vitórias de j contra i
            w_i = LpVariable(f"w_{i}_{j}_t{target_team}", 0, rem, LpInteger)
            d   = LpVariable(f"d_{i}_{j}_t{target_team}", 0, rem, LpInteger)
            w_j = LpVariable(f"l_{i}_{j}_t{target_team}", 0, rem, LpInteger)

            # Restrição: A soma dos resultados deve ser igual aos jogos restantes
            prob += (w_i + d + w_j == rem)

            # Se este jogo envolve a equipa alvo, guardamos a variável de vitória para minimizar
            if i == target_team:
                target_wins_vars.append(w_i)
            elif j == target_team:
                target_wins_vars.append(w_j)

            # Atualizar expressões de pontos para o futuro
            # Pontos de i: ganha 3 se vencer (w_i), 1 se empatar (d)
            final_points_expr[i] += 3 * w_i + d
            # Pontos de j: ganha 3 se vencer (w_j), 1 se empatar (d)
            final_points_expr[j] += 3 * w_j + d

        # --- Função Objetivo ---
        # Minimizar o número de vitórias FUTURAS da equipa alvo
        prob += lpSum(target_wins_vars)

        # --- Restrições do Campeonato ---
        # A equipa alvo deve ter pontos >= a todas as outras equipas
        # (Isso assume que 'vitória' no campeonato aceita empate de pontos. 
        # Se for necessário desempate estrito, usar >= + epsilon ou lógica extra)
        for opponent in range(1, n + 1):
            if opponent != target_team:
                prob += (final_points_expr[target_team] >= final_points_expr[opponent])

        # --- Resolver ---
        # msg=0 desliga o log do solver no terminal
        status = prob.solve(PULP_CBC_CMD(msg=0))

        # --- Output ---
        if status == LpStatusOptimal:
            # Imprime o valor da função objetivo (mínimo de vitórias necessárias)
            print(int(value(prob.objective)))
        else:
            # Impossível ganhar
            print("-1")

if __name__ == "__main__":
    solve()