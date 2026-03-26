// Analisi dati Bosoni
// ultima modifica giulia 23/03/2026 ore 11:04: corretto odine variabili
// esportate nel commento file output ultima modifica Andrea 21/03/26 ore 16:53:
// - importa anche x1x2 per calcolo distanza_2
// ultima modifica Andrea 21/03/26 ore 11:49:
// - modifica calcolo distanza nel jackknife
// ultima modifica giulia 19/03/26 ore 18:10:
// ultima modifica Andrea 18/03/26 ore 19:58:
// - aumentate cifre dopo la virgola %.lf
// ultima modifica Andrea 16/03/2026 ore 23:04
// - implementato EXIT_FAILURE per input dati
// ultimamodifica Giulia 12/03/2026 ore 10:47
// ultima modifica Andrea 12/03/2026 ore 10:24
// ultimamodifica Andrea 11/03/2026 ore 19:16
// ultimamodifica Giulia 11/03/2026 ore 11:29
// ultima modifica Andrea 09/03/26 ore 17:0
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define l                                                                      \
  6 // numero di dati per ogni riga nel file di input (se cambiato, va cambiata
    // anche la funzione di input_dati) --> aggiunto x1x2 in import
#define lj                                                                     \
  7 // FUNZIONI DA CALCOLARE numero di dati per riga nella matrice jack_array

long int conta_righe(const char *nomefile) {
  FILE *file = fopen(nomefile, "r");
  if (!file) {
    fprintf(stderr, "ERRORE: impossibile aprire il file '%s'\n", nomefile);
    return -1;
  }

  char buffer[8192];
  long int count = 0;
  size_t n;

  while ((n = fread(buffer, 1, sizeof(buffer), file)) > 0) {
    for (size_t i = 0; i < n; i++) {
      if (buffer[i] == '\n')
        count++;
    }
  }

  fclose(file);
  return count;
}

double
estrai_beta_da_file(const char *datafile) { // il file deve avere titolo:
                                            // /destinazione/beta<numero>.txt
  const char *start = strstr(datafile, "beta");
  if (!start) {
    fprintf(stderr, "Errore: 'beta' non trovato nel percorso.\n");
    return 0.0;
  }
  start += 4; // subito dopo "beta"

  char *endptr;
  double numero = strtod(start, &endptr); // legge il numero fino a dove può

  // controlla che subito dopo il numero ci sia ".txt"
  if (strncmp(endptr, ".txt", 4) != 0) {
    fprintf(stderr, "Errore: '.txt' non trovato subito dopo il numero.\n");
    return 0.0;
  }

  return numero;
}

void input_dati(char *datafile, long int term, long int sample,
                double **array) {
  FILE *file;
  double trash;
  char titolo[100];
  file = fopen(datafile, "r");
  if (file == NULL) {
    fprintf(stderr, "Errore nell'aprire il file dati %s", datafile);
  }

  // salto titolo e termalizzazione
  fgets(titolo, sizeof(titolo), file); // salto titolo
  for (long int jump = 0; jump < term; jump++) {
    fgets(titolo, sizeof(titolo), file);
  }

  // input dati
  for (long int i = 0; i < sample; i++) {
    if (fscanf(file, "%lf %lf %lf %lf %lf %lf", &array[i][0], &array[i][1],
               &array[i][2], &array[i][3], &array[i][4], &array[i][5]) != 6) {
      fprintf(stderr, "Errore lettura dati alla riga %ld\n", i);
      break;
    }
  }
} // fine input_dati

void print_array(double **array, long int righe, long int colonne) {
  printf("Inizio print_array\n");
  for (long int i = 0; i < righe; i++) {
    for (long j = 0; j < colonne; j++) {
      printf("%lf ", array[i][j]);
    }
    printf("\n");
  }
  printf("Fine print_array\n");
}

void jackknife(long int k, long int h, double **jack_array, double **array) {
  double x1 = 0, x2 = 0, segno = 0;
  double x1x2_b = 0, x1x2_f = 0;
  double sumx1 = 0, sumx2 = 0;
  double sumx1_2 = 0, sumx2_2 = 0;
  double sum_segno = 0;
  double sumx1x2_b = 0, sumx1x2_f = 0;
  double sum_distanza_b = 0, sum_distanza_f = 0;
  double sum_energia_b = 0, sum_energia_f = 0;
  double distanza_b = 0, distanza_f = 0;
  double energia_b = 0, energia_f = 0;
  long int r;

  for (long int i = 0; i < k * h; i++) {
    sumx1 += array[i][0];
    sumx1_2 += array[i][1];
    sumx2 += array[i][2];
    sumx2_2 += array[i][3];
    sumx1x2_b += array[i][5];
    sumx1x2_f += array[i][5] * (1.0 - 2.0 * (array[i][4]));
    sum_energia_b += array[i][1] + array[i][3];
    sum_energia_f += (array[i][1] + array[i][3]) * (1.0 - 2.0 * (array[i][4]));
    sum_distanza_b += (array[i][0] - array[i][2]) * (array[i][0] - array[i][2]);
    sum_distanza_f += (array[i][0] - array[i][2]) *
                      (array[i][0] - array[i][2]) * (1.0 - 2.0 * (array[i][4]));
    sum_segno += 1.0 - 2.0 * (array[i][4]);
  }

  // INIZIO jackknife su k inserito da utente
  for (long int i = 0; i < h; i++) { // i conteggio righe, h #righe
    // inizializzo i valori
    x1 = sumx1;
    x2 = sumx2;
    x1x2_b = sumx1x2_b;
    x1x2_f = sumx1x2_f;
    energia_b = sum_energia_b;
    energia_f = sum_energia_f;
    distanza_b = sum_distanza_b;
    distanza_f = sum_distanza_f;
    segno = sum_segno;

    for (long int j = 0; j < k; j++) { // j conteggio colonne, k #colonne
      r = j + i * k;
      x1 = x1 - array[r][0];
      x2 = x2 - array[r][2];
      // x1x2_b = x1x2_b - array[r][5];
      // x1x2_f = x1x2_f - array[r][5] * (1.0 - 2.0 * (array[r][4]));
      energia_b = energia_b - (array[r][1] + array[r][3]);
      energia_f = energia_f -
                  ((array[r][1] + array[r][3]) * (1.0 - 2.0 * (array[r][4])));
      distanza_b = distanza_b -
                   (array[r][0] - array[r][2]) * (array[r][0] - array[r][2]);
      distanza_f = distanza_f - (array[r][0] - array[r][2]) *
                                    (array[r][0] - array[r][2]) *
                                    (1.0 - 2.0 * (array[r][4]));
      segno = segno - (1.0 - 2.0 * (array[r][4]));
    }

    x1 = (double)x1 / (double)((h - 1) * k); // divido per "iterazioni"-k
    x2 = (double)x2 / (double)((h - 1) * k);
    x1x2_b = (double)x1x2_b / (double)((h - 1) * k);
    x1x2_f = (double)x1x2_f / (double)((h - 1) * k);
    energia_b = (double)energia_b / (double)((h - 1) * k);
    energia_f = (double)energia_f / (double)((h - 1) * k);
    distanza_b = (double)distanza_b / (double)((h - 1) * k);
    distanza_f = (double)distanza_f / (double)((h - 1) * k);
    segno = (double)segno / (double)((h - 1) * k);

    jack_array[i][0] = x1;
    jack_array[i][1] = x2;
    jack_array[i][2] = segno;
    jack_array[i][3] = energia_b;
    jack_array[i][4] = energia_f / segno;
    jack_array[i][5] = energia_b - 2 * x1x2_b;
    jack_array[i][6] = (energia_f - 2 * x1x2_f) / segno;
  } // fine iterazione su i

} // fine jackknife

int main(int argc, char **argv) {
  long int term = 0, k = 0, h = 0, sample = 0;
  double **array, **jack_array;
  double media[lj], sigma[lj];
  double beta;
  char datafile_import[80], datafile_export[80];
  FILE *file;

  // c'è da inserire a mano k e termalizzazione e nome del file da analizzare

  if (argc != 5) {
    printf("Il numero di variabili inserite è errato: inserire in ordine: "
           "termalizzazione  lunghezza_k_binning   "
           "nome_file_import  nome_file_export\n");
    return EXIT_FAILURE;
  } else {
    term = atol(argv[1]);
    k = atol(argv[2]);
    strcpy(datafile_import, argv[3]);
    strcpy(datafile_export, argv[4]);
    printf("Dati inseriti (term, k, datafile_import, datafile_export): %ld, "
           "%ld, %s, %s\n",
           term, k, datafile_import, datafile_export);
  }
  // lunghezza del file e beta
  sample = conta_righe(datafile_import) - 1; // sto levando la riga di commento
  h = (long int)(sample - term) / k;         // numero di righe
  sample = h * k;                            // lunghezza effettiva
  beta = estrai_beta_da_file(datafile_import);
  printf("Numero di sample %ld,  beta  %lf \n", sample, beta);

  // allocazione dinamica della memoria
  array = malloc((unsigned long int)sample * sizeof(double *));
  if (array == NULL) {
    perror("Errore allocazione memoria F (prima dimensione)");
    exit(EXIT_FAILURE);
  }
  for (long int i = 0; i < sample; i++) {
    array[i] = malloc((unsigned long int)l * sizeof(double));
    if (array[i] == NULL) {
      perror("Errore allocazione memoria F[i] (seconda dimensione)");
      exit(EXIT_FAILURE);
    }
  }

  jack_array = malloc((unsigned long int)h * sizeof(double *));
  if (jack_array == NULL) {
    perror("Errore allocazione memoria F (prima dimensione)");
    exit(EXIT_FAILURE);
  }
  for (long int i = 0; i < h; i++) {
    jack_array[i] = malloc((unsigned long int)lj * sizeof(double));
    if (jack_array[i] == NULL) {
      perror("Errore allocazione memoria F[i] (seconda dimensione)");
      exit(EXIT_FAILURE);
    }
  }

  // lettura dati
  input_dati(datafile_import, term, sample, array);
  // print_array(array, sample, l);

  // richiamo jackknife
  jackknife(k, h, jack_array, array);

  // calcolo media
  for (int j = 0; j < lj; j++) {
    media[j] = 0;
    for (long int i = 0; i < h; i++) {
      media[j] += jack_array[i][j];
    }
    media[j] = media[j] / (double)h;
  }

  // calcolo sigma
  for (int j = 0; j < lj; j++) {
    sigma[j] = 0;
    for (long int i = 0; i < h; i++) {
      sigma[j] += pow(media[j] - jack_array[i][j], 2);
    }
    sigma[j] = sqrt((sigma[j] * ((double)h - 1.0)) / (double)h);
  }

  // libero memoria allocata dinamicamente
  for (long int i = 0; i < sample; i++)
    free(array[i]);
  free(array);

  for (long int i = 0; i < h; i++)
    free(jack_array[i]);
  free(jack_array);

  // DEVO STAMPARE DATI SU FILE: beta, x1, sigma_x1, x2, sigma_x2, r_2,
  // sigma_r_2, segno, sigma_segno
  file = fopen(datafile_export, "a");
  if (file == NULL) {
    fprintf(stderr, "Errore nell'aprire il file dati %s", datafile_export);
  }
  // "# beta[0]   x1[1]  sigma_x1[2]   x2[3]  sigma_x2[4]  segno[5]
  // sigma_segno[6] energia_b[7] sigma_energia_b[8] energia_f[9]
  // sigma_energia_f[10] distanza_bosoni[11] sigma_distanza_bosoni[12]
  // distanza_fermioni[13] sigma_distanza_fermioni[14]
  fprintf(file,
          "%.12lf %.12lf %.12lf %.12lf %.12lf %.12lf %.12lf %.12lf %.12lf "
          "%.12lf %.12lf %.12lf %.12lf %.12lf %.12lf \n",
          beta, media[0], sigma[0], media[1], sigma[1], media[2], sigma[2],
          media[3], sigma[3], media[4], sigma[4], media[5], sigma[5], media[6],
          sigma[6]);
  fclose(file);

  return EXIT_SUCCESS;
} // end main
