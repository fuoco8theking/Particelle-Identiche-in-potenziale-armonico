#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define PI 3.141592653589
#define DIM 100000 // numero di numeri casuali da creare = 2*DIM

float random_number(float min, float max) {
  return ((float)random() / (float)RAND_MAX) * (max - min) + min;
}

int main() {

  FILE *file;
  file = fopen("boxmuller.txt", "w");
  srand(time(NULL));
  float phi[DIM], r[DIM], y1[DIM], y2[DIM], somma = 0, media = 0, varianza = 0;

  for (int i = 0; i < DIM; i++) {
    phi[i] = random_number(0, 2 * PI);
    //  printf("%f\n", phi[i]);
    r[i] = sqrt(-2 * log(random_number(0, 1)));
    y1[i] = r[i] * cos(phi[i]);
    y2[i] = r[i] * sin(phi[i]);
    fprintf(file, "%f\n %f\n", y1[i], y2[i]);
    somma += y1[i];
  }
  media = somma / DIM;
  printf("La media della distribuzione è: %f\n", media);

  fclose(file);
  // calcolo della varianza
  for (int j = 0; j < DIM; j++) {
    varianza += powf((y1[j] - media), 2);
  }
  varianza = (float)varianza / (DIM);
  printf("La varianza della distribuzione è: %f\n", varianza);
}
