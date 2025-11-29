/*********************************************************************
 * IST - ASA 25/26 - Projecto 1 - Aminoacid chain instance generator *
 *********************************************************************/
#include <iostream>

using namespace std;

// Dimensions
int _N, _M;
string aminoacids = "PNAB";

//-----------------------------------------------------------------------------

void printUsage(char *progname) {
  cerr << "Usage: " << progname << " <N> <Pmax> <seed>" << endl;
  cerr << "  N: aminoacid chain size" << endl;
  cerr << "  Pmax: maximum aminoacid potential value" << endl;
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
  if (_N < 1) {
    cerr << "ERROR: N aminoacids must be >= 1" << endl;
    printUsage(argv[0]);
  }

  sscanf(argv[2], "%d", &_M);
  if (_M < 1) {
    cerr << "ERROR: M aminoacids potential must be >= 1" << endl;
    printUsage(argv[0]);
  }

  if (argc == 4) {
    sscanf(argv[3], "%d", &seed);
    srand(seed);
  } else { // pseudo-random seed
    srand((unsigned int)time(NULL));
  }
}

inline int randomValue(int max) {
  return rand() % max; // [0, max - 1]
}

int main(int argc, char *argv[]) {
  parseArgs(argc, argv);

  // Print dimensions
  cout << _N << endl;
  // Gen aminoacid potentials
  for (int i = 0; i < _N; i++) {
    cout << (1+randomValue(_M)) << " ";
  }
  cout << endl;
  // Gen aminoacid chain
  for (int i = 0; i < _N; i++) {
    cout << aminoacids[randomValue(aminoacids.size())];
  }

  cout << endl;

  return 0;
}
