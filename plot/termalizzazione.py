import numpy as np
import matplotlib.pyplot as plt
import os
import sys


# verifica se è stato passato un argomento
if len(sys.argv) < 3:
    print("Errore: devi inserire Nt e beta, esempio: python3 termalizzazione.py 40 1.8")
    sys.exit(1)  # Esci con codice errore 1

Nt = int(sys.argv[1])  # Nt va inserito da terminale come primo argomento
beta = float(sys.argv[2])  # beta va inserito da terminale come secondo argomento


# Percorso del file con '~' (tilde) nella parte del percorso
nome_file_import = os.path.expanduser(f"~/generazione_mod3/Nt{Nt}/beta{beta}.txt")
dati = np.loadtxt(nome_file_import)

segno = dati[:, 4]
r_2 = dati[:, 0] ** 2 + dati[:, 1] ** 2
xx = np.linspace(0, len(r_2), len(r_2))
plt.errorbar(xx, r_2, fmt=".")

# mostra il grafico
plt.show()
