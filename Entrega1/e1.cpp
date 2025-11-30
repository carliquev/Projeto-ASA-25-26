#include <iostream>
#include <sstream>
#include <vector>
//#include <fstream>
#include <string>
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
int eLib(aA a, aA aEsq, aA aDir){
    return (aEsq.ePot * af(aEsq.classe, a.classe) * a.ePot  +  a.ePot * af(a.classe, aDir.classe) * aDir.ePot);
}

vector<int> eMax(vector<int> &chain){

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
    Vector<aA> aminoacidos(numAA + 2); // T inicial e final
    //Aminoacido T inicial
    aA limiteI;
    limiteI.classe = T;
    limiteI.ePot =1;
    limiteI.id =0;

    aminoacidos[0] = limiteI;


    //vector<int> pesos;
    int peso;
    for (int i = 1; i <= numAA; i++){
        ss>>peso;

    }
    while (ss >> temp){
        pesos.push_back(temp);
    }

    //Terceira linha
    string classes;
    getline(cin, classes);

    /*
    cout << "n = " << tamanhoAA << "\n";

    cout << "nums: ";

    for (int v : pesos) cout << v << " ";
    cout << "\n";

    cout << "text = " << classes << "\n";
    */







}
