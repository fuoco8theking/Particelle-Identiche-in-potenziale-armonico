from typing import ChainMap
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import sys

def f_energia_bosoni(x):
    return (np.cosh(x / 2) * np.sinh(x) ** 2 + 2 * np.cosh(x) * np.sinh(x / 2) ** 3) / (
        np.sinh(x / 2) * np.sinh(x) * (np.sinh(x) + 2 * np.sinh(x / 2) ** 2)
    )


def f_energia_fermioni(x):
    return (np.cosh(x / 2) * np.sinh(x) ** 2 - 2 * np.cosh(x) * np.sinh(x / 2) ** 3) / (
        np.sinh(x / 2) * np.sinh(x) * (np.sinh(x) - 2 * np.sinh(x / 2) ** 2)
    )


# modello
def f(x, a, b):
    return a*x + b


Nt=[20,40,60]

#------ CALCOLO LA DIMENSIONE 
dati0 = np.loadtxt(os.path.expanduser(f"~/analisi_mod3/Nt{Nt[0]}.txt"))
N_righe = dati0.shape[0]
N_colonne = len(Nt)

beta = np.zeros((N_righe, N_colonne))
eta2 = np.zeros((N_righe, N_colonne))
energia_bosoni=np.zeros((N_righe, N_colonne))
d_energia_bosoni=np.zeros((N_righe, N_colonne))
energia_fermioni=np.zeros((N_righe, N_colonne))
d_energia_fermioni=np.zeros((N_righe, N_colonne))

#i= indice di riga j= indice di colonna 
# -----------  MEMORIZZO I DATI ----------
for j in range(len(Nt)):
    nome_file_import = os.path.expanduser(
        "~/analisi_mod3/Nt" + str(Nt[j]) + ".txt"
    )
    dati = np.loadtxt(nome_file_import, skiprows=0)
    beta[:, j] = dati[:, 0]
    eta2[:, j] = (beta[:, j] / Nt[j]) ** 2
    energia_bosoni[:,j] = dati[:,7]   # energia bosoni
    d_energia_bosoni[:,j] = dati[:,8]  # errore energia bosoni
    energia_fermioni[:,j] = dati[:,9] #energia fermioni 
    d_energia_fermioni[:,j]= dati[:,10] #errore energia fermioni

# ---------  CONTROLLO CHE I BETA SIANO UGUALI 
for t in range(N_colonne):
	if (len(beta[:,t])!=len(beta[:,0])):
		print("!!!! ERRORE: NUMERO DI BETA DIVERSO PER I VARI NT")

for y in range(N_colonne):
    if not np.allclose(beta[:, y], beta[:, 0]):
        print("!!!! ERRORE: I BETA DEI VARI NT NON CORRISPONDONO !!!!")
        break
		
# -------- FACCIO I FIT CON BETA FISSATO E NT VARIABILE PER OGNI BETA 

x=[]
yb=[]
dyb=[]
yf=[]
dyf=[]

ab=[]
dab=[]
af=[]
daf=[]

dof = len(Nt) - 2
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()


with open("risultati_fit.txt", "w") as file_output:
    file_output.write("# beta   ab   err_ab af err_af  var_an_bosoni  var_an_fermioni chin_bosoni  chin_fermioni \n")

    for h in range(N_righe):
        x = eta2[h, :]
        yb = energia_bosoni[h, :]
        dyb = d_energia_bosoni[h, :]
        yf = energia_fermioni[h, :]
        dyf = d_energia_fermioni[h, :]

        parametri_bosoni, cov_bosoni = curve_fit(f, x, yb, sigma=dyb, absolute_sigma=True)

        a1, b1 = parametri_bosoni
        errori_parametri_bosoni = np.sqrt(np.diag(cov_bosoni))
        da1 = errori_parametri_bosoni[0]

        parametri_fermioni, cov_fermioni = curve_fit(f, x, yf, sigma=dyf, absolute_sigma=True)

        a2, b2 = parametri_fermioni
        errori_parametri_fermioni = np.sqrt(np.diag(cov_fermioni))
        da2 = errori_parametri_fermioni[0]

        an_bos = f_energia_bosoni(beta[h, 0])  # calcolo il valore analitico
        an_ferm = f_energia_fermioni(beta[h, 0])  # calcolo il valore analitico
        
        
        
        ax1.errorbar(x,yb,yerr=dyb,fmt='.',label=f"beta{beta[h,0]}")
        ax1.plot(x,f(x,a1,b1))
        
        ax2.errorbar(x,yf,yerr=dyf,fmt='.',label=f"beta{beta[h,0]}")
        ax2.plot(x,f(x,a2,b2))
        
        

        # -------- CHI QUADRO
        residui1 = (yb - f(x, a1, b1)) / dyb
        chi21 = np.sum(residui1**2)
        chi2n1 = chi21 / dof
        var_chi1 = np.sqrt(2 * dof)

        residui2 = (yf - f(x, a2, b2)) / dyf
        chi22 = np.sum(residui2**2)
        chi2n2 = chi22 / dof
        var_chi2 = np.sqrt(2 * dof)

        # ------- CALCOLO LA VARIAZIONE DAL VALORE ANALITICO
        var_bosoni = abs(a1 - an_bos) / da1
        var_fermioni = abs(a2 - an_ferm) / da2

        # ------- MEMORIZZO RISULTATI
        file_output.write(
            f"{beta[h,0]}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{a1}\t{da1}\t{a2}\t{da2}\t{var_bosoni}\t{var_fermioni}\t{chi2n1}\t{chi2n2}\n"
        )
        
ax1.legend() 
ax2.legend()       
plt.show()



