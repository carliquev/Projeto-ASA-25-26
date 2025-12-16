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
    // cout << "top: ";
    // for (int num: top) {
    //     cout << num << " ";
    // }
    // cout << "\n";
    //vector<vector<__uint128_t>> dp (numCruzamentos+1, vector<__uint128_t>(numCruzamentos+1, 0));
    vector<vector<pair<int, int>>> rotCam (numCamioes+1, vector<pair<int, int>>());

    // for (int i=numCruzamentos; i>0; i--) {
    //
    //
    //     for (int j = numCruzamentos; j>i; j--) {
    //         int u = top[i];
    //         int v = top[j];
    //
    //         for (int adjacente : adj[u]) {
    //
    //             if (adjacente == v) {
    //                 dp[u][v] += 1;
    //
    //             } else {
    //                 dp[u][v] += dp[adjacente][v];
    //             }
    //         }
    //     }
    // }
    //
    //
    //
    // for (int i = 1; i< numCruzamentos+1; i++) {
    //     for (int j = 1; j<numCruzamentos+1; j++) {
    //         if (i == j || dp[i][j] == 0) continue;
    //         int numCam = getNumCamiao(dp[i][j], numCamioes);
    //         if (!(numCam <m1 || numCam >m2)) {
    //             rotCam[numCam].emplace_back(pair<int, int>(i, j));
    //         }
    //     }
    // }

    for (unsigned long long i=1; i<= numCruzamentos; i++) {
        vector<__uint128_t> caminhosOrigemI (numCruzamentos+1, 0);
        caminhosOrigemI[top[i]] = 1;
        // for (int j=0; j<adj[i].size(); j++) {
        //     caminhosOrigemI[adj[i][j]] += 1;
        // }
        for (unsigned long long j=i; j<= numCruzamentos; j++) {
            if (j!=i && caminhosOrigemI[top[j]]!=0) {
                int numCam = getNumCamiao(caminhosOrigemI[top[j]], numCamioes);
                rotCam[numCam].emplace_back(top[i], top[j]);
            }
            for (int adjacente : adj[top[j]]) {
                caminhosOrigemI[adjacente] += caminhosOrigemI[top[j]];
            }
        }
    }

    for (unsigned long long i = m1; i<= m2; i++) {
        printf("C%lld", i);
        sort(rotCam[i].begin(), rotCam[i].end());
        for (pair<int, int> rot : rotCam[i]) {
            printf(" %d,%d", rot.first, rot.second);
        }

        printf("\n");

    }


    // for (int i = 0; i< numCruzamentos+1; i++) {
    //     for (int j = 0; j<numCruzamentos+1; j++) {
    //         cout << (unsigned long long)dp[i][j] << " ";
    //     }
    //     cout << endl;
    // }


    return 0;
}