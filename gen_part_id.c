// PARTICELLE IDENTICHE
// ultima modifica Andrea 21/03/26 ore 16:54:
// - aggiunta esportazione di x1x2
// ultima modifica Andrea 20/03/26 ore 9:50: piccole modifiche, sembra andare
// ultima modifica Andrea 19/03/26 ore 23:17. NUMEROSE AGGIUNTE:
// - aggiunte funzioni heatbath, microcanonico, valore_precedente
// utlima modifica giulia 19/03/26 ore 20:31
// utlima modifica Andrea 19/03/26 ore 18:38:
// - commentato update swap per test
// - commentato in metropolis per test
// ultima modifica giulia 19/03/26 ore 18:10: GRANDE CAMBIAMENTO:
// implementazione condizioni al bordo con funzione ultima modifica Andrea
// 18/03/26 ore 19:56: piccole modifiche per warnings,
// + messe 12 cifre dopo la virgola per dati esportati: %.12lf
// ultima modifica giulia 18/03/26 ore 19:31: aggiunto il 2 al
// denominatore dell'acc non twist ultima modifica Andrea 18/03/26 ore 18:18:
// NUMEROSI cambiamenti:
// - funzioni azione calcolate direttamente negli update
// - separati aggiornamenti delle due particelle nel metropolis e di conseguenza
// cambiata funzione azione
// ultima modifica Andrea 16/03/2026 ore 14:06:
// cambiamenti:
// - metropolis_update adesso fa update singolo sito
// ultima modifica Andrea 16/03/2026 or:e 23:32: cambiamenti:
// - separati update metropolis e twist
// - cambiato mis_every da 10 a 100 (tanto sono super correlati)
// ultima modifica Andrea 16/03/2026 ore 20:31: cambiamenti:
// - periodicità (come su un cerchio, senza ridondanza sito iniziale e finale)
// - delta azione twist valutata su particelle pre-update (prima era calcolata
// su quelle test)
// - levate le varie inizializzazioni inutili dei vettori test
// - riga 172: update twist da i invece che da 0
// ultima modifica giulia 16/03/26 ore 18:56
// ultima modifica Andrea 16/03/26 ore 16:23 cambiato come viene calcolato
// twisted (da guardare se cambia qualcosa) ultima modfica giulia 12/03/2026 ore
// 19:23 ULTIMA MODIFICA GIULIA 12/03/2026 ORE  15:13 cambiato delta ultima
// modifica Andrea 12/03/26 ore 10:25 (irrilevante) ULTIMA MODIFICA GIULIA
// 11/03/2026 ORE  19:18 ultima modifica Andrea 11/03/26 ore 19:16 ULTIMA
// MODIFICA GIULIA 11/03/2026 ORE  10:48 ULTIMA MODIFICA ANDREA 09/03/26 ORE
// 10:59
#include "pcg_basic.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define PI 3.141592653589 // necessario per box-muller
pcg32_random_t rng;

int rand_int(int N) { // genera un numero casuale intero tra 0 ed N-1
  // return random() % N;
  return pcg32_boundedrand_r(&rng, N);
}
double rand_double(double min, double max) {
  // genera un numero casuale float compreso tra [min,max)
  // return ((double)random() / RAND_MAX) * (max - min) + min;
  return ldexp(pcg32_random_r(&rng), -32) * (max - min) + min;
}

double gauss_norm() { // box_muller compattificato
  double phi, r, y1, y2;
  r = sqrt(-2 * log(rand_double(0 + 1.0e-16, 1)));
  phi = rand_double(0, 2 * PI);
  y1 = r * cos(phi);
  // y2 = r * sin(phi); // dato buttato
  return y1;
}

void print_array(int Nt, double *y) {
  printf("Inizio array:");
  for (int i = 0; i < Nt; i++) {
    if (i % 20 == 0) {
      printf("\n");
    }; // mando a capo ogni 10 valori
    printf("%lf ", y[i]);
  }
  printf("\nFine array.\n");
}

// funzione calcolo valori medi
void valori_medi(int Nt, double *y, double *mediaX, double *mediaX2) {
  double mX = 0, mX2 = 0;
  for (int i = 0; i < Nt; i++) {
    mX += y[i];
    mX2 += y[i] * y[i];
  }
  mX = mX / (double)Nt;
  mX2 = mX2 / (double)Nt;
  *mediaX = mX;
  *mediaX2 = mX2;
}

void prodx1x2(int Nt, double *y1, double *y2, double *x1x2) {
  double prodotto = 0;
  for (int i = 0; i < Nt; i++) {
    prodotto += y1[i] * y2[i];
  }
  *x1x2 = prodotto / (double)Nt;
}

// funzione per inizializzare gli array, uno per volta
void setup_array(int Nt, double *v, double x0) {
  for (int i = 0; i < Nt; i++) {
    v[i] = x0;
  }
}

double valore_successivo(
    int Nt, int i, int twisted, double const *const arg1,
    double const *const arg2) // arg1= particella di cui voglio calcolare il
                              // valore successivo, arg2= stampella
{

  if (i == Nt - 1 && twisted == 1) {
    return arg2[0]; // caso peggiore

  } else {
    return arg1[(i + 1) % Nt]; // seguo lo stesso cammino all'interno o al bordo
                               // senza twisted
  }
}

double valore_precedente( // ATTENZIONE
    int Nt, int i, int twisted, double const *const arg1,
    double const *const arg2) // arg1= particella di cui voglio calcolare il
                              // precedente, arg2 stampella
{
  if (i == 0 && twisted == 1) {
    return arg2[Nt - 1]; // caso peggiore
  } else if (i != 0) {
    return arg1[i - 1]; //
  } else {
    return arg1[Nt - 1];
  }
}

void heatbath(int Nt, double eta, double *y, double *ys, int twisted) {
  double sigma = 0, media = 0;
  double ym = 0, yp = 0;
  for (int i = 0; i < Nt; i++) {
    ym = valore_precedente(Nt, i, twisted, y, ys);
    yp = valore_successivo(Nt, i, twisted, y, ys);
    media = (ym + yp) / (eta * eta + 2.0); // ATTENZIONE
    sigma = sqrt(eta / (eta * eta + 2.0));
    y[i] = media + sigma * gauss_norm();
  }
}

void microcanonico(int Nt, double eta, double *y, double *ys, int twisted) {
  double media = 0;
  double ym = 0, yp = 0;
  for (int i = 0; i < Nt; i++) {
    ym = valore_precedente(Nt, i, twisted, y, ys);
    yp = valore_successivo(Nt, i, twisted, y, ys);
    media = (yp + ym) / (eta * eta + 2.0); // ATTENZIONE
    y[i] = 2.0 * media - y[i];
  }
}

// funzione per fare l'update dell' INTERO STATO
void metropolis_update(int Nt, double eta, int twisted, double *y,
                       double const *const ys, int *c1) // ys è la stampella
{
  int i = rand_int(Nt);              // scelgo sito update in modo random
  double r = rand_double(0.0, 1.0);  // numero random double tra 0 e 1
  double r2 = rand_double(0.0, 1.0); // numero random double tra 0 e 1
  double delta_azione;               // serve per entrambi i tipi di update
  double delta = sqrt(eta);
  double test;

  //   Metropolis singolo update su singola particella
  test = y[i] + (1.0 - 2.0 * r) * delta;

  // definizione valore successivo
  double yp = valore_successivo(Nt, i, twisted, y, ys); // ATTENZIONE
  // double yp = y[(i + 1) % Nt];

  // calcolo delta_azione (può essere semplificata, ma così più chiara forma)
  delta_azione = 0.5 * (eta * test * test + (pow(test - yp, 2) / eta)) -
                 0.5 * (eta * y[i] * y[i] + (pow(y[i] - yp, 2) / eta));

  if (r2 <= fmin(1, exp(-delta_azione))) {
    y[i] = test;
    (*c1)++;
  }
} // fine funzione metropolis_update

// update con twist
void twist_update(int Nt, double eta, double *y1, double *y2, int *twisted,
                  int *c2) {

  double delta_azione;               // serve per entrambi i tipi di update
  double r2 = rand_double(0.0, 1.0); // numero random double tra 0 e 1
  double tmp;
  // scelgo i -> indice distanza minima
  int i = 0;
  double min = fabs(y1[i] - y2[i]);
  double d;
  for (int k = 0; k < Nt; k++) {
    d = fabs(y1[k] - y2[k]);
    if (d < min) {
      min = d;
      i = k;
    }
  }

  // valore successivo
  double yp1 = valore_successivo(Nt, i, *twisted, y1, y2);
  double yp2 = valore_successivo(Nt, i, *twisted, y2, y1);

  // calcolo delta azione
  delta_azione =
      (0.5 / eta) * ((pow(y1[i] - yp2, 2.0) + pow(y2[i] - yp1, 2.0)) -
                     (pow(y1[i] - yp1, 2.0) + pow(y2[i] - yp2, 2.0)));

  if (r2 <= fmin(1, exp(-delta_azione))) {
    for (int l = i + 1; l < Nt;
         l++) { // twisto le particelle da i+1 --> siam sicuri ??
      tmp = y1[l];
      y1[l] = y2[l];
      y2[l] = tmp;
    }
    // *twisted = 1 - *twisted;
    *twisted = (*twisted + 1) % 2;
    (*c2)++;
  }
} // fine funzione twist_update

int main(int argc, char **argv) {
  double beta, eta;
  double distanza = 0.0, raggio2 = 0.0, segno = 0.0;
  int Nt; // dimensione lattice data da input
  long int iterazioni_update, iterazioni,
      salto = 10; // caratteristiche generazione
  double *part1, *part2;
  double x1 = 0.0, x2 = 0.0, x1_2 = 0.0, x2_2 = 0.0, x1x2 = 0.0;
  double acc_twist, acc_metropolis;
  int twisted = 0, c1 = 0, c2 = 0;
  char datafile[80];
  FILE *file;
  // srand(time(NULL));
  pcg32_srandom_r(&rng, time(NULL),
                  (intptr_t)&rng); // genera seme per numeri casuali

  if (argc != 5) {
    printf("gen_part_id: ERRORE - il numero di dati inseriti da riga di "
           "comando è errato!: inserire nel seguente ordine: beta (double) Nt "
           "(int) iterazioni (int) nome_file (char)\n");
    return EXIT_FAILURE;
  } else {
    // NUMERI INSERITI DA RIGA DI COMANDO
    beta = atof(argv[1]);
    Nt = atoi(argv[2]);
    iterazioni = atol(argv[3]);
    strcpy(datafile, argv[4]); // copio il nome del file fornito dall'esterno
  }
  printf("Valori inseriti (beta, Nt, iterazioni): %lf, %d , %ld, %s \n", beta,
         Nt, iterazioni, datafile);

  eta = beta / (double)Nt;

  // ALLOCAZIONE DINAMICA DELLA MEMORIA
  part1 = malloc((unsigned long int)(Nt) * sizeof(double));
  if (part1 == NULL) {
    fprintf(stderr, "allocation problem at (%s, %d)\n", __FILE__, __LINE__);
    return EXIT_FAILURE;
  }
  part2 = malloc((unsigned long int)(Nt) * sizeof(double));
  if (part2 == NULL) {
    fprintf(stderr, "allocation problem at (%s, %d)\n", __FILE__, __LINE__);
    return EXIT_FAILURE;
  }

  // setup vettori
  setup_array(Nt, part1, 0.1);
  setup_array(Nt, part2, 0.2);
  // apro file per scrivere dati
  file = fopen(datafile, "w");
  if (file == NULL) {
    fprintf(stderr, "Errore nell'aprire il file dati %s", datafile);
  }

  fprintf(file, "# x1[0] x1_2[1] x2[2] x2_2[3] twisted(0,1)[4] x1x2[5] \n");

  // definizione del numero di update
  iterazioni_update = iterazioni * salto;

  // RICHIAMI ALLE FUNZIONI
  for (long int n = 0; n < iterazioni_update; n++) {

    // faccio gli update metropolis
    // for (int s = 0; s < Nt; s++) { // ripeto metropolis Nt volte
    // metropolis_update(Nt, eta, twisted, part1, part2, &c1); // particella 1
    // metropolis_update(Nt, eta, twisted, part2, part1, &c1); // particella 2
    //}

    // faccio gli update heatbath e microcanonico
    if ((rand_double(0, 1) < 0.5)) {
      heatbath(Nt, eta, part1, part2, twisted);
      heatbath(Nt, eta, part2, part1, twisted);
    } else {
      for (int j = 0; j < 5; j++) {
        microcanonico(Nt, eta, part1, part2, twisted);
        microcanonico(Nt, eta, part2, part1, twisted);
      }
    }

    twist_update(Nt, eta, part1, part2, &twisted, &c2); // ATTENZIONE!!

    if (n % salto == 0) {
      // calcolo valori medi
      valori_medi(Nt, part1, &x1, &x1_2);
      valori_medi(Nt, part2, &x2, &x2_2);
      prodx1x2(Nt, part1, part2, &x1x2); // calcola il prodotto x1x2

      // debug
      raggio2 += x1_2 + x2_2;
      distanza += fabs(x1 - x2);
      segno += (1.0 - 2.0 * twisted);

      // scrivo su file
      fprintf(file, " %.12lf  %.12lf  %.12lf  %.12lf  %d  %.12lf\n", x1, x1_2,
              x2, x2_2, twisted, x1x2);
    }
  }

  // debug
  segno = segno / (double)iterazioni;
  raggio2 = raggio2 / (double)iterazioni;
  distanza = distanza / (double)iterazioni;
  printf("\n media raggio2= %lf", raggio2);
  printf("\n media distanza= %lf", distanza);
  printf("\n media segno= %lf", segno);

  // calcolo accettanza
  acc_metropolis = (double)c1 / (double)(iterazioni_update * 2 * Nt);
  acc_twist = (double)c2 / (double)iterazioni_update;
  printf("\n accettanza update Metropolis = %lf", acc_metropolis);
  printf("\n accettanza update twist = %lf \n", acc_twist);

  // chiudo file dati
  fclose(file);

  // libero memoria allocata
  free(part1);
  free(part2);

  return EXIT_SUCCESS;
}
