import random
import sys
import argparse

def gerar_input(num_equipas, num_jogos=None, seed=None):
    """
    Gera um input válido para o projeto de ASA.
    
    Args:
        num_equipas (int): Número total de equipas (n).
        num_jogos (int): Número de jogos já realizados (m). Se None, é aleatório.
        seed (int): Seed para reprodutibilidade.
    """
    if seed is not None:
        random.seed(seed)

    # Regra: As competições têm duas voltas simétricas [cite: 10]
    # Total de jogos possíveis = n * (n - 1)
    max_jogos = num_equipas * (num_equipas - 1)

    # Se o número de jogos não for especificado, escolhe um valor aleatório
    if num_jogos is None:
        num_jogos = random.randint(0, max_jogos)

    if num_jogos > max_jogos:
        raise ValueError(f"Impossível realizar {num_jogos} jogos com {num_equipas} equipas. Máximo é {max_jogos}.")

    # 1. Gerar todos os jogos possíveis (calendário completo)
    # As equipas são identificadas de 1 a n 
    todos_jogos = []
    for i in range(1, num_equipas + 1):
        for j in range(1, num_equipas + 1):
            if i != j:
                # Tuplo (Visitado, Visitante)
                todos_jogos.append((i, j))

    # 2. Selecionar aleatoriamente quais jogos já foram realizados
    jogos_realizados = random.sample(todos_jogos, num_jogos)

    # 3. Construir o output
    # Primeira linha: n m 
    output = [f"{num_equipas} {num_jogos}"]

    for casa, fora in jogos_realizados:
        # Resultado r: ID do vencedor (casa ou fora) ou 0 em caso de empate 
        # Vamos dar pesos aleatórios, ou equiprobabilidade
        opcoes_resultado = [0, casa, fora]
        resultado = random.choice(opcoes_resultado)
        
        # Linha: i j r 
        output.append(f"{casa} {fora} {resultado}")

    return "\n".join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de inputs para o Projeto ASA")
    parser.add_argument("n", type=int, help="Número de equipas")
    parser.add_argument("m", type=int, nargs='?', default=None, help="Número de jogos realizados (opcional)")
    parser.add_argument("--seed", type=int, default=None, help="Seed para o random (opcional)")
    
    args = parser.parse_args()

    try:
        conteudo = gerar_input(args.n, args.m, args.seed)
        print(conteudo)
    except ValueError as e:
        print(f"Erro: {e}", file=sys.stderr)