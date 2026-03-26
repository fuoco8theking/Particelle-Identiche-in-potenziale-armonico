# ultima modifica giulia 19/03/26 ore 18:10:
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# verifica se è stato passato un argomento
if len(sys.argv) < 5:
    print(
        "Errore: devi inserire Nt, beta, dk, colonna. esempio: python3 plot_k.py 40 1.8 100 6"
    )
    print(
        "Colonne: 2 = dx1, 4 = dx2, 6 = d(segno), 8 = d(en_b), 10 = d(en_f), 12 = d(stanza_b), 14 = d(stanza_f)"
    )
    sys.exit(1)  # Esci con codice errore 1

Nt = int(sys.argv[1])  # Nt va inserito da terminale come primo argomento
beta = float(sys.argv[2])  # beta va inserito da terminale come secondo argomento
dk = int(sys.argv[3])
colonna = int(sys.argv[4])

nome = np.array(
    [
        "errore",
        "errore",
        "sigma_x1",
        "errore",
        "sigma_x2",
        "errore",
        "sigma_segno",
        "errore",
        "sigma_en_b",
        "errore",
        "sigma_en_f",
        "errore",
        "sigma_distanza_b",
        "errore",
        "sigma_distanza_f",
        "errore",
    ]
)

nome_file_import = os.path.expanduser(f"~/analisi_mod3/errore_k_Nt{Nt}_beta{beta}")
dati = np.loadtxt(f"{nome_file_import}.txt")

r_2 = dati[:, colonna]  # in realtà è sigma_r_2
xx = np.linspace(1, len(r_2) * dk, len(r_2))  # va moltiplicato per dk
plt.errorbar(xx, r_2, fmt=".", label=nome_file_import)

# Migliorie grafiche
plt.title("Errore in funzione di k")
plt.xlabel(r"larghezza bin (k)")
plt.ylabel(nome[colonna])
plt.grid(True)
plt.legend()


# mostra il grafico
plt.show()
