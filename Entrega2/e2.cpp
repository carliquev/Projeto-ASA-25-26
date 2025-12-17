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
    vector<vector<pair<unsigned int, unsigned int>>> rotCam (m2-m1 +1, vector<pair<unsigned int, unsigned int>>());

    vector<__uint128_t> caminhosOrigemI(numCruzamentos+1, 0);
    vector<unsigned long long> isValid(numCruzamentos+1, 0);
    unsigned long long stamp = 0;

    auto getVal = [&](unsigned long long v) -> __uint128_t {
        return (isValid[v] == stamp) ? caminhosOrigemI[v] : 0;
    };

    auto addVal = [&](unsigned long long v, __uint128_t x) {
        if (isValid[v] != stamp) {
            isValid[v] = stamp;
            caminhosOrigemI[v] = x;
        } else {
            caminhosOrigemI[v] += x;

            if (caminhosOrigemI[v] > numCamioes) {
                caminhosOrigemI[v] -= numCamioes;
                // if (caminhosOrigemI[v] < 2*numCamioes) {
                //     caminhosOrigemI[v] -= numCamioes;
                // }
                // else {
                //     caminhosOrigemI[v] = caminhosOrigemI[v]%numCamioes;
                // }

            }


        }
    };

    // for (unsigned long long i=1; i<= numCruzamentos; i++) {
    //     unsigned long long v = top[i];
    //     stamp++;
    //     isValid[v] = stamp;
    //     caminhosOrigemI[v] = 1;

    //     for (unsigned long long j=1; j<= numCruzamentos; j++) {
    //         unsigned long long u = top[j];
    //         __uint128_t val = getVal(u);

    //         if (val == 0) continue;

    //         if (j!=i ) {
    //             __uint128_t numCam = getNumCamiao(val, numCamioes);
    //             if (!(numCam <m1 || numCam >m2)) {
    //                 rotCam[numCam-m1].emplace_back(v, u);
    //             }
    //         }
    //         for (unsigned long long adjacente : adj[u]) {
    //             addVal(adjacente, val);
    //         }

    //     }
    // }

    for (unsigned long long i=1; i<= numCruzamentos; i++) {
        //unsigned long long v = top[i];
        stamp++;
        isValid[i] = stamp;
        caminhosOrigemI[i] = 1;

        for (unsigned long long j=1; j<= numCruzamentos; j++) {
            unsigned long long u = top[j];
            __uint128_t val = getVal(u);

            if (val == 0) continue;
            for (unsigned long long adjacente : adj[u]) {
                addVal(adjacente, val);
            }


        }
        for(unsigned long long k =1; k <= numCruzamentos; k++){
            if(k == i || isValid[k] !=stamp){
                continue;
            }
            __uint128_t numCam =caminhosOrigemI[k]; //= getNumCamiao(caminhosOrigemI[k], numCamioes);
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


    for (unsigned long long i = 0; i <= m2-m1; i++) {
        unsigned long long numCam = m1 + i;
        printf("C%llu", numCam);
        //sort(rotCam[i].begin(), rotCam[i].end());
        for (auto &rot : rotCam[i]) {
            printf(" %u,%u", rot.first, rot.second);
        }
        printf("\n");
    }


    return 0;
}