# PLOT ENERGIA BOSONI E FERMIONI
#ultima modifica giulia 23/03/26 ore 10:58
# ultima modifica giulia 19/03/26 ore 18:10
# ultima modifica Andrea 13/03 10:33
# from typing import ChainMap
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
def energia_bosoni(x):
    return (np.cosh(x / 2) * np.sinh(x) ** 2 + 2 * np.cosh(x) * np.sinh(x / 2) ** 3) / (
        np.sinh(x / 2) * np.sinh(x) * (np.sinh(x) + 2 * np.sinh(x / 2) ** 2)
    )


def energia_fermioni(x):
    return (np.cosh(x / 2) * np.sinh(x) ** 2 - 2 * np.cosh(x) * np.sinh(x / 2) ** 3) / (
        np.sinh(x / 2) * np.sinh(x) * (np.sinh(x) - 2 * np.sinh(x / 2) ** 2)
    )


# Percorso del file con '~' (tilde) nella parte del percorso
if (Nt!=1):
	nome_file_import = os.path.expanduser(f"~/analisi_mod3/Nt{Nt}.txt")
	dati = np.loadtxt(nome_file_import, skiprows=0)  # ATTENZIONE A SKIPROWS
	Ub_data = dati[:, 7]
	dUb = dati[:, 8]
	Uf_data = dati[:, 9]
	dUf = dati[:, 10]

if (Nt==1):
	nome_file_import_bosoni = os.path.expanduser(f"risultati_fit/risultati_continuo_Energia bosoni.txt")
	dati = np.loadtxt(nome_file_import_bosoni, skiprows=0)  # ATTENZIONE A SKIPROWS
	nome_file_import_fermioni = os.path.expanduser(f"risultati_fit/risultati_continuo_Energia fermioni.txt")
	dati_fermioni = np.loadtxt(nome_file_import_fermioni, skiprows=0)  # ATTENZIONE A SKIPROWS
	Ub_data = dati[:, 1]
	dUb = dati[:, 2]
	Uf_data = dati_fermioni[:, 1]
	dUf = dati_fermioni[:, 2]

# Creazione dei valori di x
x = np.linspace(0.001, 10, 500)
x1 = dati[:, 0]

# Calcolo dei valori di y
Ub = energia_bosoni(x)
Uf = energia_fermioni(x)


# calcolo del chi quadro
resn_b = (Ub_data - energia_bosoni(x1)) / dUb
resn_f = (Uf_data - energia_fermioni(x1)) / dUf
chi_b = np.sum(resn_b**2)
chi_f = np.sum(resn_f**2)
dof = len(x1)
sigma_chi = np.sqrt(2 * dof)

# stampo il chiquadro
print("chi_bosoni = ", chi_b, sigma_chi)
print("chi_fermioni = ", chi_f, sigma_chi)
print("Gradi di libertà (dof/gdl) = ", dof)

# Disegno del grafico
plt.plot(x, Ub, "r-", label="energia interna bosoni")
plt.plot(x, Uf, "b-", label="energia interna fermioni")
plt.errorbar(
    x1,
    Ub_data,
    yerr=dUb,
    fmt=".",
    color="red",
    ecolor="red",
    label="energia interna bosoni (dati)",
)

plt.errorbar(
    x1,
    Uf_data,
    yerr=dUf,
    fmt=".",
    color="purple",
    ecolor="purple",
    label="energia interna fermioni (dati)",
)

# Migliorie grafiche
plt.title(f"Energia interna Nt {Nt}")
plt.xlabel(r"$\beta \hbar \omega$")
plt.ylabel(r"$<U/\hbar \omega>$")
plt.grid(True)
plt.legend()

plt.xlim(0, 5)  # limite asse x
plt.ylim(0, 11)  # limite asse y

# Mostra il grafico
plt.show()
