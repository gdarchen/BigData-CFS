#!/bin/bash
liste_fichiers=`ls ./*/*/*.gz`

for fichier in $liste_fichiers
do
        gunzip $fichier
done
liste_fichiers=`ls ./*/*/*`
for fichier in $liste_fichiers
do
        python2 flumetotxt.py --flume-file $fichier
done
liste_fichiers=`ls ./*/*/*.txt`
for fichier in $liste_fichiers
do
	sed -i ':a;N;$!ba;s/\n/\\n/g' $fichier
	sed -i 's/\t/\n/g' $fichier
done
liste_fichiers=`ls ./*/*/*.txt`
for fichier in $liste_fichiers
do
	sudo cp $fichier /dse/cfs/
done
