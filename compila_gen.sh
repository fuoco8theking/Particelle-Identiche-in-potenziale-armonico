#!/bin/bash

#compilazione dei singoli file
gcc gen_part_id.c pcg_basic.c -o generazione -lm -O3 -march=native -Wall -Wextra -Wconversion -fsanitize=address
