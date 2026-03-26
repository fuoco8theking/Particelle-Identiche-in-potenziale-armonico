# MEDIA VALORI GENERAZIONE
# ultima modifica Andrea 13/03 17:30
import numpy as np

# import matplotlib.pyplot as plt
import os
import sys


# Definizione della funzione
def energia_bosoni(x):
    return (np.cosh(x / 2) * np.sinh(x) ** 2 + 2 * np.cosh(x) * np.sinh(x / 2) ** 3) / (
        np.sinh(x / 2) * np.sinh(x) * (np.sinh(x) + 2 * np.sinh(x / 2) ** 2)
    )


def energia_fermioni(x):
    return (np.cosh(x / 2) * np.sinh(x) ** 2 - 2 * np.cosh(x) * np.sinh(x / 2) ** 3) / (
        np.sinh(x / 2) * np.sinh(x) * (np.sinh(x) - 2 * np.sinh(x / 2) ** 2)
    )


def segno(x):
    return (np.sinh(x / 2) ** -2 - 2 * np.sinh(x) ** -1) / (
        np.sinh(x / 2) ** -2 + 2 * np.sinh(x) ** -1
    )


# verifica se è stato passato un argomento
if len(sys.argv) < 4:
    print(
        "Errore: devi inserire Nt, beta, termalizzazione. esempio: python3 medie_gen.py 40 1.8 10000"
    )
    sys.exit(1)  # Esci con codice errore

Nt = int(sys.argv[1])  # Nt va inserito da terminale come primo argomento
beta = float(sys.argv[2])  # beta va inserito da terminale come secondo argomento
term = int(sys.argv[3])

# x1[0] x1_2[1] x2[2] x2_2[3] twisted[4]
# Percorso del file con '~' (tilde) nella parte del percorso
nome_file_import = os.path.expanduser(f"~/generazione_mod3/Nt{Nt}/beta{beta}.txt")
dati = np.loadtxt(nome_file_import, skiprows=term)


media_dati_segno = np.mean(1 - 2 * dati[:, 4])
media_energia_b = np.mean(dati[:, 1] + dati[:, 3])
media_energia_f = (
    np.mean((dati[:, 1] + dati[:, 3]) * (1 - 2 * dati[:, 4])) / media_dati_segno
)
# dati_x1 = dati[:, 0]

# dati_segno= 1+ dati_segno
# errore_dati_segno = dati[:, 8]
print("Media del segno (dati generati vs analitico)", media_dati_segno, segno(beta))
print(
    "Media Energia Bosoni (dati generati vs analitico)",
    media_energia_b,
    energia_bosoni(beta),
)
print(
    "Media Energia Fermioni (dati generati vs analitico)",
    media_energia_f,
    energia_fermioni(beta),
)
