#!/bin/bash
# per generare ciclando anche su beta inserire: Nt Nc beta0 db iterazioni(su beta):
# esempio: python3 ciclo_gen.python3 40 1000000 0.2 0.2 20
# per generare per un singolo beta (prima eseguire ./compila_gen.sh):
# esempio: ./generazione beta (double) Nt (int) iterazioni (int) nome_file (char)
# dovrebbe occupare 1.2gb circa e impiegare circa 6.75 ore
./generazione 2.0 20 10000000 ~/generazione_mod3/Nt20.txt
./generazione 2.0 40 10000000 ~/generazione_mod3/Nt40.txt
./generazione 2.0 60 10000000 ~/generazione_mod3/Nt60.txt
