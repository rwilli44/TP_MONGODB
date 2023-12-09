# TP Mongo DB - 09/12/2023 - Rachel WILLIAMS

## Étape 1: Importer les données

J'ai créé la base de données 'cinema' et la collection 'movies'. La validation de movoies fonctionne, sauf que mon regex pour l'URL de l'affiche est hyper-simplifié car je n'arrivais pas à faire plus exacte et ce n'était pas essentiel pour cet exercice.
J'ai utilisé python pour convertir les données du fichier CSV.

## Étape 2: Déclaration des classes

J'ai créé les classes Movie et Director. Par contre, j'utilise un 'view' qui s'appelle directors pour organiser les données par réalisateur et donc je n'ai pas gérée l'ajoute d'un réalisateur car en dehors de l'ajoute d'un film je ne comprenais pas le contexte pour créer un Director. J'ai quand même fait une fonctionne 'init' car je me suis dit qu'une fonctionnalité "future" de l'application pourrait être de créer un objet Director() à partir de la base de données pour être manipulée par l'application.

Dans les deux classes, ce n'était pas très claire pour moi comment controller les données. Quand je reçois les données de l'utilisateur ou du CSV, je les convertissent au bon format. Mais sinon, devrais-je utiliser des choses @property pour faire des setters ? J ne sais pas ce qui est le bon façon "pythonique" de faire ça.

## Étape 3: Création d'une collection Director

J'ai créé un "view" directors avec toute l'information des films organisée par réalisateur. Je trouvais ça plus logique qu'une collection parceque la vue se met à jour quand un film est ajouté à movies.

J'ai ajouté des méthodes demandés dans les classes Movie et Director et les 3 sont accessible à partir du menu principal qui s'affiche quand on lance le fichier main.py.

## Étape 4 : Agrégation (dans un fichier à part, utilisez la collection de votre choix)

Les quatres agrégations demandées sont faites et se trouvent dans le dossier aggregation. C'est possible aussi de les afficher à partir du menu principal. Voici les résultats des 4:
![Screenshot of the results of the first aggregation exercise ](assets\agr_1.png)
![Screenshot of the results of the second aggregation exercise ](assets\agr_2.png)
![Screenshot of the results of the third aggregation exercise ](assets\agr_3.png)
![Screenshot of the results of the fourth aggregation exercise ](assets\agr_4.png)

## Bonus : Utilisation avancées POO + Mongo

J'ai empêché la duplication d'un film avec le même titre et année dans mon code en utilisant une fonctionne qui vérifie l'existence ou non d'un film avec ces mêmes données avant d'ajouter un nouveau film. J'ai aussi empêché deux films d'avoir le même IMDB ID en le mettant en index avec unique=True.
J'ai tenté de créer un singleton dans mongodb.py, mais je ne suis pas certaine de l'avoir utilisé comme il faut dans mes classes.

Merci Cedric Jannot pour ces 3 jours de cours enrichissants.
