#include <iostream>
#include <vector>
using namespace std;



void topologicalOrder() {
    //vai dar return do vetor de ordem topologica
}


void readInputUser(int& numCruz, int& numC, int& m1, int& m2, int& numLigCruz) {
    //ler numLigCuzamentos linhas para obter os cruzamentos todos
    int A, B; //ponto A e B

    cin >> numCruz >> numC >> m1 >> m2 >>numLigCruz; //ignora whitespaces

    vector<vector<int>> adj(numCruz +2);


    for(int i =0; i < numLigCruz; i++){
        cin >> A >> B;
        //printf("%d %d\n", A, B);
        adj[A].push_back(B);
    }
    
     //debug






//guardar também adjacentes
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    int numCruzamentos; // ou seja temos o cruzmento 1 ate ao numCruzamentos
    //queremos ter o vetor adj com tamanho numCruzamentos +2
    int numCamioes; //camiao C1 ate CnumCamioes
    int m1, m2; //camioes para os quais calcular rotas, camiao m1 ate m2
    int numLigCruzamentos; // numero de ligacoes entre cruzamentos



    readInputUser(numCruzamentos, numCamioes, m1, m2, numLigCruzamentos);
    printf("%d %d %d %d", numCruzamentos, numCamioes, m1 , m2);
    return 0;
}