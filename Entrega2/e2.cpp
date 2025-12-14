#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int getNumCamiao(int numCamAB, int qtdCam) {
    return 1 + numCamAB%qtdCam;
}

vector<int> topologicalOrder(vector<vector<int>> adj) {
    vector<int> list;
    list.push_back(0);
    queue<int> q;
    int n = adj.size() -1; //-1 pois criamos adj com size +1
    vector<int> indegree(n+1, 0);

    for(int i =1; i<= n; i++) {
        for(int elem : adj[i]) {
            indegree[elem]++;
        }
    }

    for(int i =1; i<= n; i++) {
        if(indegree[i] == 0) {
            q.push(i);
        }
    }

    while (!q.empty()) {
        int top = q.front();
        q.pop();
        list.push_back(top);
        for(int elem : adj[top]) {
            indegree[elem]--;
            if (indegree[elem] == 0) {
                q.push(elem);
            }
        }
        
    }
    //vai dar return do vetor de ordem topologica


    return list;
}

vector<vector<int>> readInputUser(int& numCruz, int& numCam, int& m1, int& m2, int& numLigCruz) {
    //ler numLigCuzamentos linhas para obter os cruzamentos todos
    int A, B; //ponto A e B

    cin >> numCruz >> numCam >> m1 >> m2 >>numLigCruz; //ignora whitespaces

    vector<vector<int>> adj(numCruz +1); //+1 para  elemento 1 estar no indice 1


    for(int i =0; i < numLigCruz; i++){
        cin >> A >> B;
        //printf("%d %d\n", A, B);
        adj[A].push_back(B);
    }
    return adj;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    int numCruzamentos; // ou seja temos o cruzmento 1 ate ao numCruzamentos
    //queremos ter o vetor adj com tamanho numCruzamentos +2
    int numCamioes; //camiao C1 ate CnumCamioes
    int m1, m2; //camioes para os quais calcular rotas, camiao m1 ate m2
    int numLigCruzamentos; // numero de ligacoes entre cruzamentos

    vector<vector<int> > adj = readInputUser(numCruzamentos, numCamioes, m1, m2, numLigCruzamentos);
    // printf("%d %d %d %d", numCruzamentos, numCamioes, m1 , m2);
    vector<int> top = topologicalOrder(adj);
    // cout << "top: ";
    // for (int num: top) {
    //     cout << num << " ";
    // }
    // cout << "\n";
    vector<vector<int>> dp (numCruzamentos+1, vector<int>(numCruzamentos+1, 0));
    vector<vector<pair<int, int>>> rotCam (numCamioes+1, vector<pair<int, int>>());

    for (int i=numCruzamentos; i>0; i--) {
        for (int j = numCruzamentos; j>i; j--) {
            for (int adjacente : adj[top[i]]) {

                if (adjacente == top[j]) {
                    dp[top[i]][top[j]] += 1;

                } else {
                    dp[top[i]][top[j]] += dp[adjacente][top[j]];
                }
            }
        }
    }

    for (int i = 1; i< numCruzamentos+1; i++) {
        for (int j = 1; j<numCruzamentos+1; j++) {
            if (i == j || dp[i][j] == 0) continue;
            int numCam = getNumCamiao(dp[i][j], numCamioes);
            if (!(numCam <m1 || numCam >m2)) {
                rotCam[numCam].emplace_back(pair<int, int>(i, j));
            }
        }
    }

    for (int i = m1; i<= m2; i++) {
        printf("C%d", i);
        for (pair<int, int> rot : rotCam[i]) {
            printf(" %d,%d", rot.first, rot.second);
        }
        if (i!=m2) {
            printf("\n");
        }
    }

    //
    // for (int i = 0; i< numCruzamentos+1; i++) {
    //     for (int j = 0; j<numCruzamentos+1; j++) {
    //         cout << dp[i][j] << " ";
    //     }
    //     cout << endl;
    // }


    return 0;
}