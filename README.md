# RC2 - Activité de la recherche à Lyon


## Installation

Il est nécessaire d'avoir NodeJS et npm pour lancer le serveur.

```bash
sudo apt-get install nodejs npm
```
Il faut aussi installer MongoDB pour stocker les données et vérifier le statut

```bash
sudo apt-get install -y mongodb
sudo systemctl status mongodb
```

Si besoin, activer le service

```bash
sudo systemctl start mongodb
```

## Composition

README

Scripts --> scripts Python ayant servi pour créer des fichiers JSON exploités pour la visualisation

Siteweb --> Tout ce qui est nécessaire à l'application Web

	|views --> pages html + partials (header, footer)

	|python --> scripts lancés côté serveur

	|public --> data + images

	|nodes_modules --> modules NodeJS nécessaires au projet

## Utilisation

Dans le répertoire Siteweb, lancer la commande :

```bash
node serveur.js
```

Puis ouvrir dans un navigateur la page : http://localhost:8080

## Contribution

Simon Verdu, Vincent Toinon et Océane Jousselme

