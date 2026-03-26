# CICLO ANALISI DATI PARTICELLE IDENTICHE
# ultima modifica 21/03/26 ore 22:17 Andrea
# ULTIMA MODIFICA 12/03/26 ore 15:08 Andrea
import os
import subprocess
import logging
from datetime import datetime

# import time
import sys

# File di log
log_file = "exe_analisi.log"


# verifica se è stato passato un argomento
if len(sys.argv) < 7:
    print(
        "Errore: devi inserire   Nt   beta0  db  iterazioni(su beta)  term  k,  esempio: python3 ciclo_an.py 40 0.2 0.2 20 20000 10000"
    )
    sys.exit(1)  # Esci con codice errore 1

Nt = int(sys.argv[1])  # Nt va inserito da terminale come primo argomento
beta0 = float(sys.argv[2])  # beta va inserito da terminale come secondo argomento
db = float(sys.argv[3])
iterazioni = int(sys.argv[4])  # iterazioni su beta
term = int(sys.argv[5])
k = int(sys.argv[6])

nome_file_export = os.path.expanduser(f"~/analisi_mod3/Nt{Nt}.txt")  # File da esportare

# Imposta il logging
logging.basicConfig(
    filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s"
)


def errore(msg, iterazione):
    logging.error(f"Errore: {msg} - Iterazione: {iterazione}")
    print(f"Errore: {msg}")
    exit(1)


# Creazione della cartella se non esiste
cartella_analisi = os.path.expanduser("~/analisi_mod3")
os.makedirs(cartella_analisi, exist_ok=True)

# Inizia a scrivere nel log
logging.info("Esecuzione script analisi iniziata")
# Scrive titolo nel file esportato e cancella dati precedenti
with open(nome_file_export, "w") as f_export:
    f_export.write(
        "# beta[0]   x1[1]  sigma_x1[2]   x2[3]  sigma_x2[4]  segno[5] sigma_segno[6] en_b[7] sigma_en_b[8]  en_f[9] sigma_en_f[10]   dist_b[11]   sigma_dist_b[12]  dist_f[13]  sigma_dist_f[14]\n"
    )

# compilazione
with open(log_file, "a") as log:
    log.write(f"\n--- Compilazione {datetime.now()} ---\n")
with open(log_file, "a") as log:
    result = subprocess.run(
        [
            "gcc",
            "an_part_id.c",
            "-o",
            "analisi",
            "-lm",
            "-O3",
            "-march=native",
            "-Wall",
            "-Wextra",
            "-Wconversion",
            "-fsanitize=address",
        ],
        stdout=log,
        stderr=log,
        text=True,
    )
if result.returncode != 0:
    print("Compilazione fallita")


# Ciclo per eseguire l'analisi
for i in range(0, iterazioni):
    # Dati variabili per questa iterazione
    beta = round((db * i) + beta0, 2)
    nome_file_import = os.path.expanduser(
        f"~/generazione_mod3/Nt40/beta{beta}.txt"
    )  # File da analizzare

    # Log della configurazione
    logging.info(
        f"Esecuzione iterazione {i} con: beta = {beta}, Nt = {Nt}, term = {term}, k = {k}"
    )
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
        errore(f"Il programma ha fallito nell'iterazione {i}", i)

    # Pausa tra le iterazioni (opzionale)
    # time.sleep(1)

logging.info("Fine esecuzione script analisi")
