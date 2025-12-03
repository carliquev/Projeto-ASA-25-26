#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>
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

//Calcula afinidade(classe1, classe2)
int af(int c1, int c2){
    if (c1 == T || c2 == T) {
        return 1;
    }

    if (c1 == P){
        if (c2 == P){
            return 1;
        }
        else if (c2 == N){
            return 3;
        }
        else if (c2 == A){
            return 1;
        }
        else if (c2 == B){
            return 3;
        }
    }
    else if (c1 == N){
        if (c2 == P){
            return 5;
        }
        else if (c2 == N){
            return 1;
        }
        else if (c2 == A){
            return 0;
        }
        else if (c2 == B){
            return 1;
        }
    }
    else if (c1 == A){
        if (c2 == P){
            return 0;
        }
        else if (c2 == N){
            return 1;
        }
        else if (c2 == A){
            return 0;
        }
        else if (c2 == B){
            return 4;
        }
    }
    else if (c1 == B){
        if (c2 == P){
            return 1;
        }
        else if (c2 == N){
            return 3;
        }
        else if (c2 == A){
            return 2;
        }
        else if (c2 == B){
            return 3;
        }
    }
    return -1;
}

//Calcula a energia libertada
unsigned long long eLib(aA a, aA aEsq, aA aDir){
    return (aEsq.ePot * af(aEsq.classe, a.classe) * a.ePot  +  a.ePot * af(a.classe, aDir.classe) * aDir.ePot);
}

void seq(int i, int j, vector<vector<int>> &optK, vector<int> &res) {
    if (i>j) return;
    int k = optK[i][j];
    if (k==-1) return;
    seq(i, k-1, optK, res);
    seq(k+1, j, optK, res);
    res.push_back(k);
}

tuple<unsigned long long, vector<int>> eMax(vector<aA> &chain){
    unsigned long long maxi;
    bool first;
    int bestK, n = chain.size()-2;
    vector<int> bestSeq, seqTemp, res;
    vector<vector<unsigned long long>> dp(n+2, vector<unsigned long long> (n+2, 0));
    vector<vector<int>> optK(n+2, vector<int>(n+2, -1));
    // vector<int> sol;
    // vector<int> bestSol;


    for(int i= n; i>=1; i--){
        for(int j = 1; j<=n; j++){
            if(i>j) continue;
            maxi = 0;
            first = true;
            //vector<int> sol;
            //vector<int> bestSol;
            // sol.clear();
            // bestSol.clear();
            bestK = -1;
            vector<int> bestSeq;

            for(int k = i; k<=j; k++){
                unsigned long long e = eLib(chain[k], chain[i-1], chain[j+1]) + dp[i][k-1] + dp[k+1][j];
                if (e >= maxi) {
                    // sol = ordem[i][k-1];
                    // sol.insert(sol.end(), (ordem[k+1][j]).begin(), (ordem[k+1][j]).end());
                    // sol.push_back(k);
                    vector<int> seqTemp;
                    seq(i, k-1, optK, seqTemp);
                    seq(k+1, j, optK, seqTemp);
                    seqTemp.push_back(k);

                    if (first || e > maxi) {
                        if (first) first = false;
                        maxi = e;
                        bestK = k;
                        bestSeq = seqTemp;
                    }
                    else if (e == maxi) {
                        if (seqTemp<bestSeq) {
                            bestK = k;
                            bestSeq = seqTemp;
                        }
                    }
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
    //ios::sync_with_stdio(0);
    // cin.tie(0);

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
