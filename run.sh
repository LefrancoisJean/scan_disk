#! /bin/bash

#(($# != 1 )) && echo "Utilisation : ./run.sh [repertoireLe nom du répertoire ou '/' si root" && exit 1
#rep=$1
rep='/home/jean/Documents/'
echo "Analyse du repertoire : ${rep}"

python3 -m scan_disk -d $rep
