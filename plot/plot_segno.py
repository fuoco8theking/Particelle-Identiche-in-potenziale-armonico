#ultima modifica giulia 19/03/26 ore 18:10:
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# verifica se è stato passato un argomento
if len(sys.argv) < 2:
    print("Errore: devi inserire Nt esempio: python3 esempio.py 40 \n PER PLOT LIM CONTINUO NT= 1 \n")
    sys.exit(1)  # Esci con codice errore

Nt = int(sys.argv[1])  # Nt va inserito da terminale come primo argomento


# Definizione della funzione
def segno(x):
    return (np.sinh(x / 2) ** -2 - 2 * np.sinh(x) ** -1) / (
        np.sinh(x / 2) ** -2 + 2 * np.sinh(x) ** -1
    )


# Percorso del file con '~' (tilde) nella parte del percorso
if(Nt!=1):
	nome_file_import = os.path.expanduser(f"~/analisi_mod3/Nt{Nt}.txt")
	dati = np.loadtxt(nome_file_import)
	dati_segno = dati[:, 5]
	errore_dati_segno = dati[:, 6]
if(Nt==1):
	nome_file_import = os.path.expanduser(f"risultati_fit/risultati_continuo_Segno.txt")
	dati = np.loadtxt(nome_file_import)
	dati_segno = dati[:, 1]
	errore_dati_segno = dati[:, 2]




# Creazione dei valori di x
x = np.linspace(0.001, 10, 500)
x1 = dati[:, 0]  # beta

# Calcolo dei valori di y
y = segno(x)


# calcolo del chi quadro
resn = (dati_segno - segno(x1)) / errore_dati_segno
chi = np.sum(resn**2)
dof = len(x1)
sigma_chi = np.sqrt(2 * dof)

# stampo il chiquadro
print("chi_segno = ", chi, sigma_chi)
print("Gradi di libertà (dof/gdl) = ", dof)

# Disegno del grafico
plt.plot(x, y, "r-")
plt.errorbar(x1, dati_segno, yerr=errore_dati_segno, fmt=".", label=" segno (dati)")


# Migliorie grafiche
plt.title(f"Segno dato dal twist estremi cammino Nt {Nt}")
plt.xlabel(r"$\beta \hbar \omega$")
plt.ylabel(r"$<(-1)^{twist}>$")
plt.grid(True)
plt.legend()

plt.xlim(0, 5)  # limite asse x
plt.ylim(0, 1)  # limite asse y

# Mostra il grafico
plt.show()
