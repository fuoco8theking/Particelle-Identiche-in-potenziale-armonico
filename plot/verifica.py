import numpy as np

# import matplotlib.pyplot as plt
import os
import sys


# verifica se è stato passato un argomento
if len(sys.argv) < 2:
    print("Errore: devi inserire Nt beta esempio: python3 esempio.py 40 1.0")
    sys.exit(1)  # Esci con codice errore

Nt = int(sys.argv[1])  # Nt va inserito da terminale come primo argomento
beta= float(sys.argv[2])

nome_file_import = os.path.expanduser(f"~/generazione_mod3/Nt{Nt}/beta{beta}.txt")
dati = np.loadtxt(nome_file_import, skiprows=1)

print(dati[:,4])

media= np.mean(dati[:,4])
print(media)
