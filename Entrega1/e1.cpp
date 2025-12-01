#include <iostream>
#include <sstream>
#include <vector>
//#include <fstream>
#include <string>
#include <tuple>
using namespace std;

#define T 0
#define P 1
#define N 2
#define A 3
#define B 4

struct aA {
    int id;
    int ePot;
    int classe;
};

//Calcula afinidade(classe1, classe2)
long long af(int c1, int c2){
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
long long eLib(aA a, aA aEsq, aA aDir){
    return (aEsq.ePot * af(aEsq.classe, a.classe) * a.ePot  +  a.ePot * af(a.classe, aDir.classe) * aDir.ePot);
}

tuple<long long, vector<vector<int>>> eMax(vector<aA> chain){
    int changed;
    long long maxi=0;
    int n = chain.size()-2;
    vector<vector<long long>> dp(n+2, vector<long long> (n+2, 0)); //reduzir um destes (meter so n em vez de n+2 e ver se tamos ou nao a sair da matriz)
    vector<vector<vector<int>>> ordem(n+2, vector<vector<int>>(n+2, vector<int>())); //reduzir um destes

    vector<vector<int>> sols;

    for(int i= n; i>=1; i--){ // i = n-1; i>=0
        for(int j = 1; j<=n; j++){ // j<n
            if(i>j) continue;
            changed = 0;
            maxi = 0;
            vector<int> sol;
            for(int k = i; k<=j; k++){
                long long e = eLib(chain[k], chain[i-1], chain[j+1]) + dp[i][k-1] + dp[k+1][j];
                if (e >= maxi) {
                    if (e == maxi) {
                        changed = 1;
                    }
                    if (e > maxi) {
                        changed = 2;
                    }
                    maxi = e;
                    sol = ordem[i][k-1];
                    sol.insert(sol.end(), (ordem[k+1][j]).begin(), (ordem[k+1][j]).end());
                    sol.push_back(k);
                }
            }
            // Se e == maxi
            if (changed == 1) {
                sols.push_back(sol);
                dp[i][j]= maxi;
                ordem[i][j] = sol;
            // Se e > maxi
            } else if (changed == 2) {
                sols.clear();
                sols.push_back(sol);
                dp[i][j]= maxi;
                ordem[i][j] = sol;
            }




        }

    }

    return {dp[1][n], sols};
}

int main(){
    //Ler input dos testes
    //Primeira linha
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
    limiteI.id =0;

    aminoacidos[0] = limiteI;

    //Terceira linha
    string classes;
    getline(cin, classes);

    //vector<int> pesos;
    int peso;
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
        aminoacidos[i].id = i;
        aminoacidos[i].classe = tipo;
        aminoacidos[i].ePot = peso;
        i++;
    }
    aA limiteF;
    limiteF.classe = T;
    limiteF.ePot =1;
    limiteF.id =i;
    aminoacidos[i] = limiteF;


    tuple<long long, vector<vector<int>>> result = eMax(aminoacidos);

    cout<<get<0>(result)<<endl;

    vector<vector<int>> v = std::get<1>(result);
    vector<int> y = v[0];


    for (size_t i =0; i<y.size();i++) {
        if (i != y.size() - 1) {
            cout<< y[i] << " ";
        }else {
            cout<< y[i] << "\n";
        }
    }




    return 0;




}
