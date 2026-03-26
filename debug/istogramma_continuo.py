import matplotlib.pyplot as plt
import numpy as np

# Nome del file
nome_file = "indice_i.txt"

# Legge il contenuto
with open(nome_file, "r") as f:
    contenuto = f.read()

# Converte in lista di float (dati continui)
lista = list(map(float, contenuto.split()))

# Calcolo media e varianza
media = float(np.mean(lista))
varianza = float(np.var(lista))

print(f"Media: {media}")
print(f"Varianza: {varianza}")

# Istogramma continuo
plt.hist(lista, bins=200, edgecolor="black")

plt.title("Distribuzione dei dati continui")
plt.xlabel("Valore")
plt.ylabel("Frequenza")

# Mostra media sull'istogramma
plt.axvline(
    media, color="red", linestyle="dashed", linewidth=1, label=f"Media = {media:.2f}"
)
plt.legend()

plt.show()
