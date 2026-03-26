#!/bin/bash

#compilazione file di generazione
echo "Inizio compilazione file analisi"
gcc an_part_id.c -o analisi -lm -O3 -march=native -Wall -Wextra -Wconversion -fsanitize=address
echo "Fine compilazione file analisi"
echo "Per eseguire: ./analisi termalizzazione  lunghezza_k  nome_file_import  nome_file_export"
