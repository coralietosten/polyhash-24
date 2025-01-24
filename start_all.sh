#!/bin/bash

clear

# Les fichiers d'entrée
inputs=(
    "data/a_example.in"
    "data/b_small.in"
    "data/c_medium.in"
    "data/d_final.in"
)

# En-tête
echo -e "\nPolyhash team B \n"
echo -e "+-------------------+------------------------+------------+--------+--------+"
echo -e "| Fichier           | Un ballon par altitude | Aléatoire  | Proche | Proche |"
echo -e "+-------------------+------------------------+------------+--------+--------+"

for input in "${inputs[@]}"; do
    result=$(python3 main.py "$input")
    
    un_ballon=$(echo "$result" | grep "Un ballon par altitude" | awk '{print $NF}')
    aleatoire=$(echo "$result" | grep "Aléatoire" | awk '{print $NF}')
    proche=$(echo "$result" | grep "Proche" | awk '{print $NF}')
    prochev2=$(echo "$result" | grep "Proche v2" | awk '{print $NF}')
    
    printf "| %-17s | %-22s | %-10s | %-6s | %-6s |\n" "$input" "$un_ballon" "$aleatoire" "$proche" "$prochev2"
done

echo -e "+-------------------+------------------------+------------+--------+--------+"
