# PLOT DISTANZA BOSONI E FERMIONI
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# verifica se è stato passato un argomento
if len(sys.argv) < 2:
    print("Errore: devi inserire Nt esempio: python3 esempio.py 40 \n PER PLOT LIM CONTINUO NT= 1 \n")
    sys.exit(1)  # Esci con codice errore

Nt = int(sys.argv[1])  # Nt va inserito da terminale come primo argomento


def distanza_2(x, segno):
    return 2 / np.tanh(x) - segno




# Percorso del file con '~' (tilde) nella parte del percorso
if (Nt!=1):
	nome_file_import = os.path.expanduser(f"~/analisi_mod3/Nt{Nt}.txt")
	dati = np.loadtxt(nome_file_import, skiprows=0)  # ATTENZIONE A SKIPROWS
	Db_data = dati[:, 11]
	dDb = dati[:, 12]
	Df_data = dati[:, 13]
	dDf = dati[:, 14]

if (Nt==1):
	nome_file_import_bosoni = os.path.expanduser(f"risultati_fit/risultati_continuo_Distanza bosoni.txt")
	dati = np.loadtxt(nome_file_import_bosoni, skiprows=0)  # ATTENZIONE A SKIPROWS
	nome_file_import_fermioni = os.path.expanduser(f"risultati_fit/risultati_continuo_Distanza fermioni.txt")
	dati_fermioni = np.loadtxt(nome_file_import_fermioni, skiprows=0)  # ATTENZIONE A SKIPROWS
	Db_data = dati[:, 1]
	dDb = dati[:, 2]
	Df_data = dati_fermioni[:, 1]
	dDf = dati_fermioni[:, 2]

# Creazione dei valori di x
x = np.linspace(0.001, 10, 500)
x1 = dati[:, 0]

# Calcolo analitici dei valori y ()
Db = distanza_2(x, +1)
Df = distanza_2(x, -1)


# calcolo del chi quadro
resn_b = (Db_data - distanza_2(x1, 1)) / dDb
resn_f = (Df_data - distanza_2(x1, -1)) / dDf
chi_b = np.sum(resn_b**2)
chi_f = np.sum(resn_f**2)
dof = len(x1)
sigma_chi = np.sqrt(2 * dof)

# stampo il chiquadro
print("chi_bosoni = ", chi_b, sigma_chi)
print("chi_fermioni = ", chi_f, sigma_chi)
print("Gradi di libertà (dof/gdl) = ", dof)

# Disegno del grafico
plt.plot(x, Db, "r-", label="quadrato distanza bosoni")
plt.plot(x, Df, "b-", label="quadrato distanza fermioni")
plt.errorbar(
    x1,
    Db_data,
    yerr=dDb,
    fmt=".",
    color="red",
    ecolor="red",
    label="quadrato distanza bosoni (dati)",
)

plt.errorbar(
    x1,
    Df_data,
    yerr=dDf,
    fmt=".",
    color="purple",
    ecolor="purple",
    label="quadrato distanza fermioni (dati)",
)

# Migliorie grafiche
plt.title(f"Distanza al quadrato Nt {Nt}")
plt.xlabel(r"$\beta \hbar \omega$")
plt.ylabel(r"$<D^2 \omega m / \hbar>$")
plt.grid(True)
plt.legend()

plt.xlim(0, 5)  # limite asse x
plt.ylim(0, 12)  # limite asse y

# Mostra il grafico
plt.show()
