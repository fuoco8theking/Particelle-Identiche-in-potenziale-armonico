# import matplotlib.pyplot as plt
#
## Nome del file (mettilo nella stessa cartella dello script)
# nome_file = "indice_i.txt"
#
## Legge tutto il contenuto del file
# with open(nome_file, "r") as f:
#    contenuto = f.read()
#
## Converte automaticamente in lista di interi
# lista = list(map(int, contenuto.split()))
#
## Istogramma
# plt.hist(lista, bins=range(41), align="left", edgecolor="black")
#
# plt.title("Istogramma dei numeri")
# plt.xlabel("Valore")
# plt.ylabel("Frequenza")
#
# plt.show()

import matplotlib.pyplot as plt
from collections import Counter

# Nome del file (stessa cartella dello script)
nome_file = "indice_i.txt"

# Legge tutto il contenuto del file
with open(nome_file, "r") as f:
    contenuto = f.read()

# Converte in lista di interi (numeri separati da spazio)
lista = list(map(int, contenuto.split()))

# Conta le occorrenze esatte
conteggi = Counter(lista)

# Prepara i dati da 0 a 39
x = list(range(40))
y = [conteggi[i] for i in x]

# Grafico a barre (discreto, preciso)
plt.bar(x, y, edgecolor="black")

plt.title("Distribuzione dei numeri (0-39)")
plt.xlabel("Valore")
plt.ylabel("Frequenza")

plt.xticks(range(40))  # mostra tutti i numeri sull'asse x

plt.show()
