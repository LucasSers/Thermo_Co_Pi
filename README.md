# Thermomètre Connecté

## Description

Une sonde de température branchée à un Raspberry Pi relève la température à un intervalle régulier.
Ces températures sont stockées dans un fichier avec la date et l'heure du relevé. 
Dans le format suivant : `aaaa-mm-jj hh:mm:ss;tempEnCelsius`.
Le Raspberry Pi distribue sur demande à tout appareil, les relevés via le WiFi.
L'application Android récupère ces relevés, les traite et affiche :

* La dernière température relevée
* Les extremums des températures du jour actuel
> (avec possibilité de changer d'unités)
* Un graphique des relevés sur demande
## Membres de l'équipe

+ Dorian _PRODUCT OWNER_
+ Jérémy   _DEVELOPPEUR_
+ Lucas _SCRUM MASTER_
+ Valentin _DEVELOPPEUR_

## Lien vers le board Zenhub (Android)
https://app.zenhub.com/workspaces/thermo-co-pi-61a90875bd9c34001e8dc8b1/board

## Lien vers le dossier Google Drive
https://drive.google.com/drive/folders/12q8LObpDJC4tdu51sZCCLXz2jUl-ETXE

## Lien vers le dépôt de l'application Raspberry Android
https://github.com/LucasSers/Thermo_Co_Android
