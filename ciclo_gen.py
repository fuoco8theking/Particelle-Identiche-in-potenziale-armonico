# CICLO GENERAZIONE DATI PARTICELLE IDENTICHE
# ULTIMA MODIFICA ANDREA 12/03/26 ore 15:07
import os
import subprocess
import logging
from datetime import datetime
import time
import sys

# verifica se è stato passato un argomento
if len(sys.argv) < 6:
    print(
        "Errore: devi inserire Nt Nc beta0 db iterazioni(su beta), esempio: python3 ciclo_gen.py 40 1000000 0.2 0.2 20"
    )
    sys.exit(1)  # Esci con codice errore 1

Nt = int(sys.argv[1])  # Nt va inserito da terminale come primo argomento
Nc = int(sys.argv[2])
beta0 = float(sys.argv[3])  # beta va inserito da terminale come secondo argomento
db = float(sys.argv[4])
iterazioni = int(sys.argv[5])

# File di log
log_file = "exe_generazione.log"


# Imposta il logging
logging.basicConfig(
    filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s"
)


def errore(msg, iterazione):
    logging.error(f"Errore: {msg} - Iterazione: {iterazione}")
    print(f"Errore: {msg}")
    exit(1)


# Inizia a scrivere nel log
logging.info("Esecuzione script iniziata")

# Elimino file rimasti da vecchie generazioni e ricreo la cartella
cartella_generazione = os.path.expanduser(f"~/generazione_mod3/Nt{Nt}")
os.makedirs(cartella_generazione, exist_ok=True)
for file in os.listdir(cartella_generazione):
    file_path = os.path.join(cartella_generazione, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

# compilazione
with open(log_file, "a") as log:
    log.write(f"\n--- Compilazione {datetime.now()} ---\n")
with open(log_file, "a") as log:
    result = subprocess.run(
        [
            "gcc",
            "gen_part_id.c",
            "pcg_basic.c",
            "-o",
            "generazione",
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


# Ciclo per eseguire il programma
for i in range(0, iterazioni):
    # Dati variabili per questa iterazione
    beta = round((db * i) + beta0, 2)
    nome_file = os.path.join(cartella_generazione, f"beta{beta}.txt")

    # Log della configurazione
    logging.info(
        f"Esecuzione iterazione {i} con: beta={beta}, Nt={Nt}, Nc={Nc}, nome_file={nome_file}"
    )

    # Esegui il programma con i dati variabili
    try:
        result = subprocess.run(
            ["./generazione", str(beta), str(Nt), str(Nc), nome_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        logging.info(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        errore(f"Il programma ha fallito nell'iterazione {i}", i)

    # Pausa tra le iterazioni
    # time.sleep(1)

logging.info("Tutte le iterazioni sono state completate correttamente.")
