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

struct aA {
    unsigned long long ePot;
    int classe;
};

int af(int c1, int c2) {
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

void seq(int i, int j, vector<vector<int>> &optK, vector<int> &res) {
    if (i>j) return;
    int k = optK[i][j];
    seq(i, k-1, optK, res);
    seq(k+1, j, optK, res);
    res.push_back(k);
}

tuple<unsigned long long, vector<int>> eMax(vector<aA> &chain){
    unsigned long long maxi;
    bool first;
    int bestK, n = chain.size()-2;
    vector<int> res;
    vector<vector<unsigned long long>> dp(n+2, vector<unsigned long long> (n+2, 0));
    vector<vector<int>> optK(n+2, vector<int>(n+2, -1));

    for(int i= n; i>=1; i--){
        for(int j = 1; j<=n; j++){
            if(i>j) continue;
            maxi = 0;
            first = true;
            bestK = -1;

            for(int k = i; k<=j; k++){
                unsigned long long e = eLib(chain[k], chain[i-1], chain[j+1]) + dp[i][k-1] + dp[k+1][j];
                if (e >= maxi) {
                    if (first) first = false;
                    maxi = e;
                    bestK = k;
                }
            }
            dp[i][j] = maxi;
            optK[i][j] = bestK;
        }
    }
    seq(1, n, optK, res);
    return {dp[1][n], res};
}


vector<aA> readinputUser(){
    int numAA;

    cin >> numAA; // Lê tamanho do aminoacido
    cin.ignore();

    //Segunda linha
    string pesosAA;
    getline(cin, pesosAA);
    stringstream ss(pesosAA);

    vector<aA> aminoacidos(numAA + 2); // T inicial e final
    //Aminoacido T inicial
    aA limiteI;
    limiteI.classe = T;
    limiteI.ePot =1;

    aminoacidos[0] = limiteI;

    //Terceira linha
    string classes;
    getline(cin, classes);

    //vector<int> pesos;
    unsigned long long peso;
    int tipo=1;
    int i =1;
    for (char c : classes) {
        ss>>peso;
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
        aminoacidos[i].classe = tipo;
        aminoacidos[i].ePot = peso;
        i++;
    }
    aA limiteF;
    limiteF.classe = T;
    limiteF.ePot =1;
    aminoacidos[i] = limiteF;
    return aminoacidos;
}


int main(){
    ios::sync_with_stdio(0);
     cin.tie(0);

    //Ler input dos testes
    //Primeira linha
    
    vector<aA> chain = readinputUser();

    tuple<unsigned long long, vector<int>> result = eMax(chain);
    unsigned long long x = get<0>(result);
    cout<<x<<endl;

    vector<int> v = get<1>(result);


    for (size_t i =0; i<v.size();i++) {
        if (i != v.size() - 1) {
            cout<< v[i] << " ";
        }else {
            cout<< v[i] << "\n";
        }
    }
    return 0;
}
