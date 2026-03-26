from typing import ChainMap
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import sys
import logging
from matplotlib.figure import Figure

logging.basicConfig(
    filename="exe_fit.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    filemode="a"
)

# verifica se è stato passato un argomento
if len(sys.argv) < 3:
    print("Errore: devi inserire l'osservabile e beta esempio: python3 esempio.py 2 1.8 \n segno= 5 \n energia bosoni= 7 \n energia fermioni= 9 \n distanza bosoni= 11 \n distanza fermioni= 13\n")
    sys.exit(1)  # Esci con codice errore

indice_osservabile = int(sys.argv[1])  # va inserito da terminale come primo argomento
beta_inserita= float(sys.argv[2])

#osservabile 7 
def energia_bosoni(x):
    return (np.cosh(x / 2) * np.sinh(x) ** 2 + 2 * np.cosh(x) * np.sinh(x / 2) ** 3) / (
        np.sinh(x / 2) * np.sinh(x) * (np.sinh(x) + 2 * np.sinh(x / 2) ** 2)
    )

#osservabile 9
def energia_fermioni(x):
    return (np.cosh(x / 2) * np.sinh(x) ** 2 - 2 * np.cosh(x) * np.sinh(x / 2) ** 3) / (
        np.sinh(x / 2) * np.sinh(x) * (np.sinh(x) - 2 * np.sinh(x / 2) ** 2)
    )
 #osservabile 11 e 13 
def distanza_2(x, segno):
    return 2 / np.tanh(x) - segno

# osservabile 5
def f(x, a, b):
    return b*x + a
    
def segno(x):
    return (np.sinh(x / 2) ** -2 - 2 * np.sinh(x) ** -1) / (
        np.sinh(x / 2) ** -2 + 2 * np.sinh(x) ** -1
    )


Nt=[10,20,40,60,80,100] # CAMBIARE SE NECESSARIO

#------ CALCOLO LA DIMENSIONE 
dati0 = np.loadtxt(os.path.expanduser(f"~/analisi_mod3/Nt{40}.txt")) #quello che sono sicura che ha il massimo dei beta 
N_righe = dati0.shape[0]
N_colonne = len(Nt)



beta = np.zeros((N_righe, N_colonne))
eta2 = np.zeros((N_righe, N_colonne))
osservabile=np.zeros((N_righe, N_colonne))
d_osservabile=np.zeros((N_righe, N_colonne))


#i= indice di riga j= indice di colonna 
# -----------  MEMORIZZO I DATI ----------
for j in range(len(Nt)):
    nome_file_import = os.path.expanduser(
        "~/analisi_mod3/Nt" + str(Nt[j]) + ".txt"
    )

    dati = np.loadtxt(nome_file_import, skiprows=0)

    # sistema il caso 1D
    if dati.ndim == 1:
        dati = dati.reshape(1, -1)

    # padding / taglio (SEMPRE eseguito)
    m, k = dati.shape
    nuovo = np.zeros((N_righe, k))
    nuovo[:min(m, N_righe)] = dati[:min(m, N_righe)]
    dati = nuovo

    beta[:, j] = dati[:, 0]
    eta2[:, j] = (beta[:, j] / Nt[j]) ** 2
    osservabile[:, j] = dati[:, indice_osservabile]
    d_osservabile[:, j] = dati[:, indice_osservabile + 1]



# ---------  CONTROLLO CHE I BETA SIANO UGUALI 
for t in range(N_colonne):
	if (len(beta[:,t])!=len(beta[:,0])):
		print("!!!! ERRORE: NUMERO DI BETA DIVERSO PER I VARI NT")

for y in range(N_colonne):
    if not np.allclose(beta[:, y], beta[:, 0]):
        print("!!!! ERRORE: I BETA DEI VARI NT NON CORRISPONDONO !!!!")
        break
        

# inizializza il vettore
indice_beta = -1 * np.ones(len(Nt), dtype=int)  # -1 = non trovato

for u in range(len(Nt)):
    # trova gli indici dove beta[:, u] è vicino a beta_inserita
    match = np.where(np.isclose(beta[:, u], beta_inserita))[0]

    if len(match) > 0:
        indice_beta[u] = match[0]  # prendo il primo match
    # se non c'è match rimane -1
    if indice_beta[u] == -1:
     print(f"Valore non trovato nel file Nt{Nt[u]}")
    

#calcolo valore analitico
if (indice_osservabile==5):
	a_an= segno(beta_inserita)
if (indice_osservabile==7):
	a_an= energia_bosoni(beta_inserita)
if (indice_osservabile==9):
	a_an= energia_fermioni(beta_inserita)
if (indice_osservabile==11):
	a_an= distanza_2(beta_inserita,1)
if (indice_osservabile== 13):
	a_an= distanza_2(beta_inserita,-1)
	
#creo etichetta 
etichette = {
    5: "Segno",
    7: "Energia bosoni",
    9: "Energia fermioni",
    11: "Distanza bosoni",
    13: "Distanza fermioni"
}

nome_osservabile = etichette[indice_osservabile]

# -------- FACCIO I FIT CON BETA FISSATO E NT VARIABILE PER BETA SCELTO 

x = np.zeros(len(Nt))
y = np.zeros(len(Nt))
dy = np.zeros(len(Nt))

for j in range(len(Nt)):
    idx = indice_beta[j]
    if idx == -1:
        print(f"ATTENZIONE: beta_inserita non trovato per Nt={Nt[j]}")
        x[j] = np.nan
        y[j] = np.nan
        dy[j] = np.nan
    else:
        x[j] = eta2[idx, j]
        y[j] = osservabile[idx, j]
        dy[j] = d_osservabile[idx, j] 

print(y)
dof = len(Nt) - 2

with open(f"risultati_fit/risultati_fit_oss{indice_osservabile}_beta{beta_inserita}.txt", "w") as file_output:
    
    file_output.write("# beta   a   err_a  var_an  chi \n")

    parametri, cov = curve_fit(f, x, y, sigma=dy, absolute_sigma=True, maxfev=10000)
    a, b = parametri

    errori_parametri = np.sqrt(np.diag(cov))
    da = errori_parametri[0]

    plt.title(f"{nome_osservabile} (beta={beta_inserita})")
    plt.errorbar(x, y, yerr=dy, fmt='.', label=f"beta{beta_inserita}")
    x1=np.linspace(0,max(x),10)
    plt.plot(x1, f(x1, a, b))
    plt.ylabel(nome_osservabile)
    plt.xlabel(r"$\eta^2$")
    plt.savefig(f"immagini_fit/fit_{nome_osservabile}_beta={beta_inserita}.png")

    # -------- CHI QUADRO
    residui = (y - f(x, a, b)) / dy
    chi2 = np.sum(residui**2)
    chi2n = chi2 / dof
    var_chi = np.sqrt(2 * dof)

    # ------- CALCOLO LA VARIAZIONE DAL VALORE ANALITICO
    var_an = abs(a - a_an) / da

    # ------- MEMORIZZO RISULTATI
    file_output.write(f"{beta_inserita}\t{a}\t{da}\t{var_an}\t{chi2n}\n")
    print(f"beta= {beta_inserita} \n a= {a} +/- {da} \n a_an= {a_an} \n")

    
    logging.info(
     f"beta={beta_inserita}, a={a} +/- {da}, var={var_chi}, "
     f"a_an={a_an}, var_an={var_an}, chi2n={chi2n}"
     )
plt.legend()
plt.show()

