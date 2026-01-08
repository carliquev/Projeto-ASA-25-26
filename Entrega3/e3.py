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
                if i < j:
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

    # Para cada equipa, resolver o problema de otimização
    for equipa_alvo in range(1, n_equipas + 1):
        resultado = resolver_para_equipa(equipa_alvo, n_equipas, pontos, games_left)
        print(resultado)


def resolver_para_equipa(equipa_alvo, n_equipas, pontos_atuais, games_left):
    """
    Resolve o problema de PL para uma equipa específica.
    Retorna o número mínimo de vitórias necessárias ou -1 se impossível.
    """
    
    # Criar o problema de minimização
    prob = pulp.LpProblem(f"Equipa_{equipa_alvo}", pulp.LpMinimize)
    
    # Variáveis: para cada jogo restante, quem ganha
    # Para cada par (i,j) com i<j e games_left[(i,j)] > 0
    # Criamos variáveis para cada instância do jogo
    
    jogo_vars = {}  # (i, j, instancia) -> {home_win, away_win, draw}
    
    for (i, j), count in games_left.items():
        for inst in range(count):
            # Variáveis binárias para cada resultado possível
            home_win = pulp.LpVariable(f"hw_{i}_{j}_{inst}", cat='Binary')
            away_win = pulp.LpVariable(f"aw_{i}_{j}_{inst}", cat='Binary')
            draw = pulp.LpVariable(f"d_{i}_{j}_{inst}", cat='Binary')
            
            jogo_vars[(i, j, inst)] = {
                'home_win': home_win,
                'away_win': away_win,
                'draw': draw
            }
            
            # Restrição: exatamente um resultado por jogo
            prob += home_win + away_win + draw == 1, f"one_result_{i}_{j}_{inst}"
    
    # Calcular pontos finais de cada equipa
    pontos_finais = {}
    
    for equipa in range(1, n_equipas + 1):
        pontos_finais[equipa] = pontos_atuais[equipa]
        
        # Adicionar pontos dos jogos restantes
        for (i, j), count in games_left.items():
            for inst in range(count):
                vars_jogo = jogo_vars[(i, j, inst)]
                
                if equipa == i:
                    # Equipa é a casa
                    pontos_finais[equipa] += 3 * vars_jogo['home_win'] + vars_jogo['draw']
                elif equipa == j:
                    # Equipa é o visitante
                    pontos_finais[equipa] += 3 * vars_jogo['away_win'] + vars_jogo['draw']
    
    # Contar vitórias da equipa alvo nos jogos restantes
    vitorias_alvo = 0
    
    for (i, j), count in games_left.items():
        for inst in range(count):
            vars_jogo = jogo_vars[(i, j, inst)]
            
            if equipa_alvo == i:
                vitorias_alvo += vars_jogo['home_win']
            elif equipa_alvo == j:
                vitorias_alvo += vars_jogo['away_win']
    
    # Função objetivo: minimizar vitórias da equipa alvo
    prob += vitorias_alvo, "Minimizar_Vitorias"
    
    # Restrições: equipa alvo deve ter mais pontos que todas as outras
    # (ou pelo menos empatar, assumindo critérios de desempate favoráveis)
    for outra_equipa in range(1, n_equipas + 1):
        if outra_equipa != equipa_alvo:
            prob += pontos_finais[equipa_alvo] >= pontos_finais[outra_equipa] + 0.01, \
                    f"ganhar_{outra_equipa}"
    
    # Resolver o problema
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    # Verificar se foi encontrada solução viável
    if prob.status == pulp.LpStatusOptimal:
        return int(pulp.value(vitorias_alvo))
    else:
        return -1


if __name__ == "__main__":
    solve()

