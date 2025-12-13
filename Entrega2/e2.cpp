#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int getNumCamiao(int numCAB, int numCam) {
    return 1 + numCAB%numCam;
}

vector<int> topologicalOrder(vector<vector<int>> adj) {
    vector<int> list;
    queue<int> q;
    int n = adj.size() -1; //-1 pois criamos adj com size +1
    vector<int> indegree(n+1, 0);

    for(int i =1; i< n; i++) {
        for(int elem : adj[i]) {
            indegree[elem]++;
        }
    }

    for(int i =1; i< n; i++) {
        if(indegree[i] == 0) {
            q.push(i);
        }
    }

    while (!q.empty()) {
        int top = q.front();
        q.pop();
        for(int elem : adj[top]) {
            indegree[elem]--;
            if (indegree[elem] == 0) {
                q.push(elem);
            }
        }
        list.push_back(top);
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
    vector<int>topOrder = topologicalOrder(adj);
    // for (int num: topOrder) {
    //     cout << num << " ";
    // }

    vector<vector<int>> dp (numCamioes+1, vector<int>(numCamioes+1, 0));


    return 0;
}