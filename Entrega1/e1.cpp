#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <tuple>
using namespace std;

#define T 0
#define P 1
#define N 2
#define A 3
#define B 4

struct aA { //Aminoacidos que vao compor a cadeia
    unsigned long long ePot; 
    int classe;
};

int af(int c1, int c2) { 
    //Tabela para obter a afinidade entre duas classes de aminoacidos
    //As primeira linha e coluna correspondem a classe T
    int AF[5][5] = {
        {1, 1, 1, 1, 1},
        {1, 1, 3, 1, 3},
        {1, 5, 1, 0, 1},
        {1, 0, 1, 0, 4},
        {1, 1, 3, 2, 3}
    };
    return AF[c1][c2];
}

//Calcula a energia libertada
unsigned long long eLib(aA a, aA aEsq, aA aDir){
    return (aEsq.ePot * af(aEsq.classe, a.classe) * a.ePot  +  a.ePot * af(a.classe, aDir.classe) * aDir.ePot);
}


//Constroi o a sequencia pela qual os aminoacidos devem ser removidos
void seq(int i, int j, vector<vector<int>> &optK, vector<int> &res) {
    if (i>j) return;
    int k = optK[i][j];
    seq(i, k-1, optK, res); //Construir recursivamente a esquerda e direita
    seq(k+1, j, optK, res);
    res.push_back(k);
}

tuple<unsigned long long, vector<int>> eMax(vector<aA> &cadeia){
    //Calcula a energia maxima e guarda as energias maximas de cada subsequencia
    //Guarda tambem o indice do ultimo elemento a ser removido para cada subsequencia
    unsigned long long maxi;
    int bestK, n = cadeia.size()-2;
    vector<int> res; //Vetor utilizado para guardar a sequencia final de remocao
    vector<vector<unsigned long long>> dp(n+2, vector<unsigned long long> (n+2, 0)); //Matriz de energias
    vector<vector<int>> optK(n+2, vector<int>(n+2, -1)); //Matriz de indices

    for(int i= n; i>=1; i--){
        for(int j = 1; j<=n; j++){
            if(i>j) continue;
            maxi = 0;
            bestK = -1;

            for(int k = i; k<=j; k++){
                unsigned long long e = eLib(cadeia[k], cadeia[i-1], cadeia[j+1]) + dp[i][k-1] + dp[k+1][j];
                if (e >= maxi) {
                    maxi = e;
                    bestK = k;
                }
            }
            dp[i][j] = maxi;
            optK[i][j] = bestK;
        }
    }
    seq(1, n, optK, res);
    return {dp[1][n], res}; //Devolve um tuplo com a energia e a sequencia de aminoacidos a retirar
}


vector<aA> readinputUser(){
    int numAA;

    cin >> numAA; // Le tamanho do aminoacido
    cin.ignore();

    //Recebe as energias potencias dos aminoacidos
    string ePotAA;
    getline(cin, ePotAA);
    stringstream ss(ePotAA);

    vector<aA> cadeia(numAA + 2); // n+2 para o T inicial e final
    //Aminoacido T inicial
    aA limiteI;
    limiteI.classe = T;
    limiteI.ePot =1;

    cadeia[0] = limiteI;

    //Recebe as classes dos aminoacidos
    string classes;
    getline(cin, classes);

    unsigned long long ePot;
    int tipo=1;
    int i =1;
    for (char c : classes) {
        //Coloca na cadeia todos os aminoacidos introduzidos
        ss>>ePot;
        switch (c) {
            case 'A':
                tipo = A; break;
            case 'B':
                tipo = B; break;
            case 'N':
                tipo = N; break;
            case 'P':
                tipo = P; break;
            default:
                break;
        }
        cadeia[i].classe = tipo;
        cadeia[i].ePot = ePot;
        i++;
    }
    //Coloca na cadeia o T final
    aA limiteF;
    limiteF.classe = T;
    limiteF.ePot =1;
    cadeia[i] = limiteF;

    return cadeia;
}


int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    vector<aA> cadeia = readinputUser();

    tuple<unsigned long long, vector<int>> result = eMax(cadeia);
    unsigned long long x = get<0>(result);
    //Imprime a energia libertada maxima
    cout<<x<<endl;

    vector<int> v = get<1>(result);

    /*Percorre o vetor da melhor sequencia de remocao 
    e imprime os indices do aminoacido a remover*/
    for (size_t i =0; i<v.size();i++) {
        if (i != v.size() - 1) {
            cout<< v[i] << " ";
        }else {
            //Caso seja o ultimo colocar newline
            cout<< v[i] << "\n";
        }
    }
    return 0;
}
