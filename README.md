[[Relazione (modIII)]]

[[codice generazione Bonati]]
	- [[spiegazione struttura funzione Node e init_conf (chat-gpt)]]
[[codice analisi bosoni Bonati]]
[[codice analisi fermioni bonati]]

[[Struttura generale]]
[[Generazione dati (modIII)]]
[[Analisi dati (modIII)]]

# stime quantitative 
Per effettuarle è sufficiente osservare i log e i dati generati
## spazio occupato dalla Generazione
  considerando la scrittura di 5 colonne di dati con 6 cifre dopo la virgola (per le prime 4) e la 5 colonna 1/0, si ottiene:
  $10^6$ righe <--> 39.1 Mb
## tempo di Generazione
  - considerando la generazione **sul server** di $20*10^6$ righe stampate (con stampa ogni `mis_every`=10), il tempo necessario è circa 30 min (non sembra dipendere in modo significativo da beta (e forse non ci dipende minimamente)):
  $10^6$ righe <--> 9 $s$
- considerando generazione sul **computer di Andrea** modalità performance, $1*10^6$ righe stampate (stampa ogni `mis_every`= 10), il tempo necessario è stato 55 secondi:
  $10^6$ campionamenti <--> 5.5 $s$

- INPUT: file dati `~/generazione_mod3/Nt40/beta#.#.txt`,
contenente `iterazioni` righe di `x1` `x1_2` `x2` `x2_2` `twisted`
- OUTPUT: file dati `~/analisi_mod3/Nt#.txt`, contenente una riga di: `beta[0]   x1[1]  sigma_x1[2]   x2[3]  sigma_x2[4]  r_2[5] sigma_r_2[6] segno[7] sigma_segno[8]  distanza[9] sigma_distanza[10]   energia_f[11]   sigma_energia_f[12]`

# struttura del file di Analisi

#### long int conta_righe(const char *nomefile)
  Conta le righe del file di testo passato a funzione
#### double estrai_beta_da_file(const char *datafile)
  Estrae il valore di beta dal titolo del file di testo passato a funzione "cercando" nel titolo tra `beta` e `.txt`
#### void input_dati(char *datafile, long int term, long int sample, double **array)
  Importa i dati dal file di testo, tenendo conto del fatto che la prima riga è il titolo e saltando le righe di termalizzazione
#### void print_array(double **array, long int righe, long int colonne) 
  Stampa sul terminale l'array passato a funzione (debug)
#### void jackknife(long int k, long int h, double **jack_array, double **array) 
  Crea `h` sample da cui estrarre media ed errore delle quantità: `x1` `x2` `energia_b` `segno` `distanza_b` `energia_f`
#### int main(int argc, char **argv) 
