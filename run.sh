#! /bin/bash

#(($# != 1 )) && echo "Utilisation : ./run.sh [repertoireLe nom du répertoire ou '/' si root" && exit 1
#rep=$1
rep='/home/jean/Documents/'
echo "Analyse du repertoire : ${rep}"

# sudo docker run -it --rm -v $PWD:/code pyrt3.6:3.0.2 python -m scan_disk -d $rep

python3 -m scan_disk -d $rep
