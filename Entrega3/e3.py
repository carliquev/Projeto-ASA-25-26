import pulp;
import sys;


def read_input():
    for line in sys.stdin:
        for token in line.split():
            yield token




def main():
    input_reader = read_input()

    n_equipas = int(next(input_reader))
    m_jogos = int(next(input_reader))


    pontos_equipas = [0] * n_equipas
    needed_games = [-1] * n_equipas


    for i in range(1, m_jogos + 1):
        equipa_atual = int(next(input_reader))
        adversario = int(next(input_reader))
        resultado = int(next(input_reader))
        if resultado == 0:
            pontos_equipas[equipa_atual-1] += 1
            pontos_equipas[adversario-1] += 1
        elif resultado == equipa_atual:
            pontos_equipas[equipa_atual-1] += 3
        elif resultado == adversario:
            pontos_equipas[adversario-1] += 3
    
    maxi = max(pontos_equipas)

    for i in range(n_equipas):
        if pontos_equipas[i]  == maxi:
            needed_games[i] = 0

    for ponto in pontos_equipas:
        print(ponto)



if __name__ == "__main__":
    main()


