#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

unsigned  getNumCamiao(__uint64_t numCamAB, unsigned  qtdCam) {
    return 1 + numCamAB%qtdCam;
}

vector<unsigned > topologicalOrder(vector<vector<unsigned >> adj) {
    vector<unsigned > list;
    list.push_back(0);
    queue<unsigned > q;
    unsigned  n = adj.size() -1; // -1 pois criamos adj com size +1
    vector<unsigned > indegree(n+1, 0);

    for(unsigned  i =1; i<= n; i++) {
        for(unsigned  elem : adj[i]) {
            indegree[elem]++;
        }
    }

    for(unsigned  i =1; i<= n; i++) {
        if(indegree[i] == 0) {
            q.push(i);
        }
    }

    while (!q.empty()) {
        unsigned  top = q.front();
        q.pop();
        list.push_back(top);
        for(unsigned  elem : adj[top]) {
            indegree[elem]--;
            if (indegree[elem] == 0) {
                q.push(elem);
            }
        }
        
    }
    //vai dar return do vetor de ordem topologica
    return list;
}

vector<vector<unsigned >> readInputUser(unsigned & numCruz, unsigned & numCam, unsigned & m1, unsigned & m2, unsigned & numLigCruz) {
    //ler numLigCuzamentos linhas para obter os cruzamentos todos
    unsigned  A, B; //ponto A e B

    cin >> numCruz >> numCam >> m1 >> m2 >>numLigCruz; //ignora whitespaces

    vector<vector<unsigned >> adj(numCruz +1); //+1 para  elemento 1 estar no indice 1


    for(unsigned  i =0; i < numLigCruz; i++){
        cin >> A >> B;
        adj[A].push_back(B);
    }
    return adj;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    unsigned  numCruzamentos; // ou seja temos o cruzmento 1 ate ao numCruzamentos
    //queremos ter o vetor adj com tamanho numCruzamentos +2
    unsigned  numCamioes; //camiao C1 ate CnumCamioes
    unsigned  m1, m2; //camioes para os quais calcular rotas, camiao m1 ate m2
    unsigned  numLigCruzamentos; // numero de ligacoes entre cruzamentos

    vector<vector<unsigned > > adj = readInputUser(numCruzamentos, numCamioes, m1, m2, numLigCruzamentos);
    vector<unsigned > top = topologicalOrder(adj);
    vector<vector<pair<unsigned, unsigned>>> rotCam (m2-m1 +1, vector<pair<unsigned, unsigned>>());

    vector<__uint64_t> caminhosOrigemI(numCruzamentos+1, 0);
    vector<unsigned > isValid(numCruzamentos+1, 0);
    unsigned  stamp = 0;

    auto getVal = [&](unsigned  v) -> __uint64_t {
        return (isValid[v] == stamp) ? caminhosOrigemI[v] : 0;
    };

    auto addVal = [&](unsigned  v, __uint64_t x) {
        if (isValid[v] != stamp) {
            isValid[v] = stamp;
            caminhosOrigemI[v] = x;
        } else {
            caminhosOrigemI[v] += x;

            if (caminhosOrigemI[v] > numCamioes) {
                // mais rápido do que fazer %
                caminhosOrigemI[v] -= numCamioes;

            }
        }
    };

    for (unsigned  i=1; i<= numCruzamentos; i++) {
        stamp++;
        isValid[i] = stamp;
        caminhosOrigemI[i] = 1;

        for (unsigned  j=1; j<= numCruzamentos; j++) {
            unsigned  u = top[j];
            __uint64_t val = getVal(u);

            if (val == 0) continue;
            for (unsigned  adjacente : adj[u]) {
                addVal(adjacente, val);
            }
        }

        for(unsigned  k =1; k <= numCruzamentos; k++){
            if(k == i || isValid[k] !=stamp){
                continue;
            }
            __uint64_t numCam =caminhosOrigemI[k]; //= getNumCamiao(caminhosOrigemI[k], numCamioes);
            if(numCam == numCamioes){
                numCam =1;
            }else{
                numCam++;
            }
            if (!(numCam <m1 || numCam >m2)) {
                rotCam[numCam-m1].emplace_back(i, k);
            }
        }
    }

    for (unsigned  i = 0; i <= m2-m1; i++) {
        unsigned  numCam = m1 + i;
        printf("C%u", numCam);
        for (auto &rot : rotCam[i]) {
            printf(" %u,%u", rot.first, rot.second);
        }
        printf("\n");
    }

    return 0;
}