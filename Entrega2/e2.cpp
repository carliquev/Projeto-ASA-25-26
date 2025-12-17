#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

unsigned long long getNumCamiao(__uint128_t numCamAB, unsigned long long qtdCam) {
    return 1 + numCamAB%qtdCam;
}

vector<unsigned long long> topologicalOrder(vector<vector<unsigned long long>> adj) {
    vector<unsigned long long> list;
    list.push_back(0);
    queue<unsigned long long> q;
    unsigned long long n = adj.size() -1; // -1 pois criamos adj com size +1
    vector<unsigned long long> indegree(n+1, 0);

    for(unsigned long long i =1; i<= n; i++) {
        for(unsigned long long elem : adj[i]) {
            indegree[elem]++;
        }
    }

    for(unsigned long long i =1; i<= n; i++) {
        if(indegree[i] == 0) {
            q.push(i);
        }
    }

    while (!q.empty()) {
        unsigned long long top = q.front();
        q.pop();
        list.push_back(top);
        for(unsigned long long elem : adj[top]) {
            indegree[elem]--;
            if (indegree[elem] == 0) {
                q.push(elem);
            }
        }
        
    }
    //vai dar return do vetor de ordem topologica


    return list;
}

vector<vector<unsigned long long>> readInputUser(unsigned long long& numCruz, unsigned long long& numCam, unsigned long long& m1, unsigned long long& m2, unsigned long long& numLigCruz) {
    //ler numLigCuzamentos linhas para obter os cruzamentos todos
    unsigned long long A, B; //ponto A e B

    cin >> numCruz >> numCam >> m1 >> m2 >>numLigCruz; //ignora whitespaces

    vector<vector<unsigned long long>> adj(numCruz +1); //+1 para  elemento 1 estar no indice 1


    for(unsigned long long i =0; i < numLigCruz; i++){
        cin >> A >> B;
        //printf("%d %d\n", A, B);
        adj[A].push_back(B);
    }
    return adj;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    unsigned long long numCruzamentos; // ou seja temos o cruzmento 1 ate ao numCruzamentos
    //queremos ter o vetor adj com tamanho numCruzamentos +2
    unsigned long long numCamioes; //camiao C1 ate CnumCamioes
    unsigned long long m1, m2; //camioes para os quais calcular rotas, camiao m1 ate m2
    unsigned long long numLigCruzamentos; // numero de ligacoes entre cruzamentos

    vector<vector<unsigned long long> > adj = readInputUser(numCruzamentos, numCamioes, m1, m2, numLigCruzamentos);
    vector<unsigned long long> top = topologicalOrder(adj);

    vector<vector<pair<unsigned long long, unsigned long long>>> rotCam (m2-m1 +1);
    unsigned long long valAtual;

    for (unsigned long long origem = 1; origem <= numCruzamentos; ++origem) {

        vector<__uint128_t> caminhos(numCruzamentos + 1, 0);
        caminhos[origem] = 1;

        // percorre SEMPRE a topológica completa
        for (unsigned long long k = 1; k <= numCruzamentos; ++k) {
            unsigned long long v = top[k];
    
            if (caminhos[v] == 0) continue;
    
            // // Decide o camião para (origem, v)
            // if (v != origem) {
            //     unsigned long long cam = getNumCamiao(caminhos[v], numCamioes);
            //     if (cam >= m1 && cam <= m2) {
            //         rotCam[cam - m1].emplace_back(origem, v);
            //     }
            // }

            // Relaxação (contagem de caminhos): propaga para sucessores
            for (unsigned long long adjacente : adj[v]) {
                valAtual = caminhos[v];
                if (valAtual > numCamioes) {
                    if (valAtual < 2*numCamioes) {
                        valAtual -= numCamioes;
                    } else if (valAtual % numCamioes != 0) {
                        valAtual %=numCamioes;
                    }
                }
                caminhos[adjacente] +=valAtual;
            }

        }
        for (unsigned long long destino = 1; destino <= numCruzamentos; ++destino) {
            if (destino == origem) continue;
            if (caminhos[destino] == 0) continue;

            unsigned long long cam = getNumCamiao(caminhos[destino], numCamioes);
            if (cam < m1 || cam > m2) continue;

            rotCam[cam - m1].emplace_back(origem, destino);
        }
    }


    for (unsigned long long i = 0; i < m2 - m1 + 1; ++i) {
        unsigned long long cam = m1 + i;
        printf("C%llu", cam);
        for (auto &p : rotCam[i]) {
            printf(" %llu,%llu", p.first, p.second);
        }
        printf("\n");
    }
    
    return 0;
}
