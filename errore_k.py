## ERRORE IN FUNZIONE DI k_binning
#ultima modifica giulia 19/03/26 ore 18:10:
# ultima modifica 14/03/26 14:18 Andrea
# ultima modifica 12/03/26 11:04 andrea
import os
import subprocess
import logging
from datetime import datetime
import time
import sys

## per vedere i risultati eseguire poi plot_k.py

# File di log
log_file = "exe_errore_k.log"

# verifica se è stato passato un argomento
if len(sys.argv) < 6:
    print(
        "Errore: devi inserire Nt beta termalizzazione k_max dk, esempio: python3 errore_k.py 40 1.8 1000 20000 100"
    )
    sys.exit(1)  # Esci con codice errore 1

Nt = int(sys.argv[1])  # Nt va inserito da terminale come primo argomento
beta = float(sys.argv[2])  # beta va inserito da terminale come secondo argomento
term = int(sys.argv[3])
k_max = int(sys.argv[4])
dk = int(sys.argv[5])

# Variabili
k_min = 1
nome_file_export = os.path.expanduser(
    f"~/analisi_mod3/errore_k_Nt{Nt}_beta{beta}.txt"
)  ## SISTEMARE

# Scrive titolo e cancella dati precedenti
with open(nome_file_export, "w") as f_export:
    f_export.write(
        "# beta[0]   x1[1]  sigma_x1[2]   x2[3]  sigma_x2[4] segno[5] sigma_segno[6]  energia_b[7]  sigma_energia_b[8]  energia_f[9] sigma_energia_f[10] distanza_b[11] sigma_distanza_b[12]   distanza_f[13]   sigma_distanza_f[14]\n"
    )

# Creazione della cartella se non esiste
cartella_analisi = os.path.expanduser("~/analisi_mod3")
os.makedirs(cartella_analisi, exist_ok=True)

# Imposta il logging
logging.basicConfig(
    filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s"
)


def errore(msg, iterazione):
    logging.error(f"Errore: {msg} - Iterazione: {iterazione}")
    print(f"Errore: {msg}")
    exit(1)


# Inizia a scrivere nel log
logging.info("Esecuzione script analisi iniziata")


# Ciclo per eseguire l'analisi
for k in range(k_min, k_max, dk):
    # Dati variabili per questa iterazione: k
    nome_file_import = os.path.expanduser(
        f"~/generazione_mod3/Nt{Nt}/beta{beta}.txt"
    )  # File da analizzare

    # Log della configurazione
    logging.info(f"Esecuzione iterazione {k} con: beta={beta}, Nt={Nt}")
    logging.info(f"nome_file_import = {nome_file_import}")
    logging.info(f"nome_file_export = {nome_file_export}")

    # Esegui il programma con i dati variabili
    try:
        result = subprocess.run(
            ["./analisi", str(term), str(k), nome_file_import, nome_file_export],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        logging.info(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        errore(f"Il programma ha fallito nell'iterazione {k}", k)

    # Pausa tra le iterazioni (opzionale)
    # time.sleep(1)

logging.info("Fine esecuzione script analisi")
