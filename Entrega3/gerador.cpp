/**********************************************************************
 * IST - ASA 25/26 - Projecto 3 - Instance Generator - Pedro Monteiro *
 **********************************************************************/
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
using namespace std;

int _N; // # teams
int _P; // prob of a game having been played
struct Game { int i, j, r; };

//-----------------------------------------------------------------------------

void printUsage(char *progname) {
  cerr << "Usage: " << progname << " <N> <P> [seed]" << endl;
  cerr << "  N: number of teams >= 2" << endl;
  cerr << "  P: probability of a game having been played (0-100)" << endl;
  cerr << "  seed: random seed number (optional)" << endl;
  exit(1);
}

void parseArgs(int argc, char *argv[]) {
  int seed = 0;

  if (argc < 3 || argc > 4) {
    cerr << "ERROR: Wrong number of arguments" << endl;
    printUsage(argv[0]);
  }

  sscanf(argv[1], "%d", &_N);
  if (_N < 2) {
    cerr << "ERROR: N must be >= 2" << endl;
    printUsage(argv[0]);
  }

  sscanf(argv[2], "%d", &_P);
  if (_P < 0 || _P > 100) {
    cerr << "ERROR: Probability must be between 0 and 100" << endl;
    printUsage(argv[0]);
  }

  if (argc == 4) {
    sscanf(argv[3], "%d", &seed);
    srand(seed);
  } else { 
    srand((unsigned int)time(NULL));
  }
}

inline int randomValue(int max) {
  if (max == 0) return 0;
  return rand() % max; // [0, max - 1]
}

int main(int argc, char *argv[]) {
  parseArgs(argc, argv);
  vector<Game> games;

  for (int i = 1; i <= _N; i++) { // O(N^2) - todos contra todos
    for (int j = 1; j <= _N; j++) {
      if (i == j || randomValue(100) >= _P) continue;
      int resultType = randomValue(3); // 0, 1, ou 2
      int result = 0;

      if (resultType == 0)      result = 0; // empate
      else if (resultType == 1) result = i; // vitória i
      else                      result = j; // vitória j
      games.push_back({i, j, result});
    }
  }

  cout << _N << " " << games.size() << endl;
  for (size_t k = 0; k < games.size(); k++)
      cout << games[k].i << " " << games[k].j << " " << games[k].r << endl;
  return 0;
}
