import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import sys
import subprocess
import glob
import logging

logging.basicConfig(
    filename="exe_fit.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Programma avviato")

# ---------------- INPUT
if len(sys.argv) < 2:
    print("Errore: devi inserire l'osservabile esempio: python3 esempio.py 2 1.8 \n segno= 5 \n energia bosoni= 7 \n energia fermioni= 9 \n distanza bosoni= 11 \n distanza fermioni= 13\n")
    sys.exit(1)  # Esci con codice errore

valore_input = int(sys.argv[1])

# ---------------- ETICHETTE
etichette = {
    5: "Segno",
    7: "Energia bosoni",
    9: "Energia fermioni",
    11: "Distanza bosoni",
    13: "Distanza fermioni"
}

nome_osservabile = etichette[valore_input]

# ---------------- DATI 
Nt = 40  # deve essere incluso in quelli da analizzare, serve per prendere beta 

dati0 = np.loadtxt(os.path.expanduser(f"~/analisi_mod3/Nt{Nt}.txt"))
beta0 = dati0[:, 0]

N_righe = dati0.shape[0]

logging.info("Inizio i fit")

# ---------------- LOOP FIT
for i in range(N_righe):
    try:
        logging.info(f"Fit per beta = {beta0[i]}")
        
        subprocess.run([
            "python3",
            "fit_Nt_uno.py",
            str(valore_input),
            str(beta0[i])
        ], check=True)

        logging.info(f"OK beta = {beta0[i]}")

    except Exception as e:
        logging.error(f"Errore beta = {beta0[i]}: {e}")
        
        
logging.info("Finito i fit")

files = sorted(glob.glob(f"risultati_fit/risultati_fit_oss{valore_input}_beta*.txt"))
with open(f"risultati_fit/risultati_continuo_{nome_osservabile}.txt", "w") as out:
    for file_name in sorted(files):
        with open(file_name, "r") as inp:
            for line in inp:
                line = line.strip()
                if line and not line.startswith("#"):
                    out.write(line)
            out.write("\n")
