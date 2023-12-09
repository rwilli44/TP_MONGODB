# Standard Library Imports
import csv

# Third-Party Iports
from progress.spinner import MoonSpinner
from pymongo.collection import Collection
from pymongo.database import Database


# Local Imports
from models.mongodb import MongoDB
from models.movie import Movie


# Schèma pour valider les données de la collection movies
movies_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "title",
            "year",
            "summary",
            "short_summary",
            "imdb_id",
            "runtime",
            "rating",
            "url_poster",
            "director",
        ],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "Le titre ('title') est obligatoire et doit être une chaîne de caractères.",
            },
            "year": {
                "bsonType": "int",
                "minimum": 1888,
                "maximum": 3000,
                "description": "L'année ('year') est obligatoire et doit être une chaîne de caractères composée de 4 chiffres.",
            },
            "summary": {
                "bsonType": "string",
                "description": "Le résumé ('summary') du film est obligatoire et doit être une chaîne de caractères.",
            },
            "court_summary": {
                "bsonType": "string",
                "description": "Le résumé court ('short_summary') du film est obligatoire et doit être une chaîne de caractères.",
            },
            "imdb_id": {
                "bsonType": "string",
                "pattern": "[A-Za-z0-9]{9}",
                "description": "L'ID du site IMDB ('id_imdb') du film est obligatoire et doit être une chaîne de neuf caractères alphanumériques.",
            },
            "runtime": {
                "bsonType": "int",
                "description": "La duration du film ('runtime') est obligatoire et doit être un nombre entier.",
            },
            "trailer": {
                "bsonType": "string",
                "description": "L'identifiant YouTube de la bande-annonce du film ('trailer') n'est pas obligatoire et doit être une chaîne de caractères.",
            },
            "rating": {
                "bsonType": "double",
                "minimum": 0,
                "maximum": 10.0,
                "description": "La note du publique d'IMDB du film ('rating') est obligatoire et doit être un double.",
            },
            "url_poster": {
                "bsonType": "string",
                "pattern": "https?:\/\/.+jpg",  # This is not specific enough but I didn't want to spend all weekend on regex
                "description": "L'url pour l'affiche du film ('poster_url') n'est pas obligatoire et doit être une chaîne de caractères.",
            },
            "director": {
                "bsonType": "string",
                "description": "Le réalisateur ou la réalisatrice du film ('director') est obligatoire et doit être une chaîne de caractères.",
            },
            "writers": {
                "bsonType": "array",
                "uniqueItems": True,
                "description": "La liste de scénariste(s) du film ('writers') n'est pas obligatoire et doit être un tableau de chaines de caractères uniques.",
                "items": {
                    "bsonType": "string",
                    "description": "Les noms des sécnaristes doivent être des chaînes de caractères.",
                },
            },
            "cast": {
                "bsonType": "array",
                "uniqueItems": True,
                "description": "La liste des acteurs du film ('cast') n'est pas obligatoire et doit être un tableau de chaines de caractères uniques.",
                "items": {
                    "bsonType": "string",
                    "description": "Les noms des acteurs doivent être des chaînes de caractères.",
                },
            },
        },
    },
}


#### FONCTIONNES pour gérer la collection et la vue


def add_validator(collection: str, validator_schema: dict) -> None:
    """Ajoute une schèma de validation à une collection.
    Args:
        collection (str): nom de la collection
        validator_schema (dict): schèma JSON pour décrire et valider les données de la collection
    """
    connection: MongoDB = MongoDB()
    db: Database = connection.get_DB()
    db.command("collMod", collection, validator=validator_schema)
    print("validator added to movies collection")


def create_directors_view() -> None:
    """Créer un view des réalisateurs à partir de la collection movies."""
    connection: MongoDB = MongoDB()
    db: Database = connection.get_DB()
    pipeline: list[dict] = [
        {"$group": {"_id": "$director", "movies": {"$push": "$$ROOT"}}},
        {"$project": {"movies": {"director": 0}}},
    ]
    db.command({"create": "directors", "viewOn": "movies", "pipeline": pipeline})
    print("directors view created in cinema database")


def create_unique_index(collection_name: str, index_element: str) -> None:
    """Create an index in the given collection on the given element with unique
    set to true.

    Args:
        collection_name (str): name of the collection
        index_element (str): the element on which to set the index
    """
    connection: MongoDB = MongoDB()
    db: Database = connection.get_DB()
    collection: Collection = db[collection_name]
    collection.create_index([(index_element)], unique=True)
    print(
        f"unique index created on item {index_element} in the {collection_name} collection"
    )


def create_movies_collection() -> None:
    """Créer une collection qui s'appelle movies.
    Si la collection existe déjà une erreur affiche."""
    connection: MongoDB = MongoDB()
    db: Database = connection.get_DB()
    try:
        db.create_collection("movies")
        print("movies collection created in cinema database")
    except Exception as e:
        print(e)


def load_movies_from_csv(fichier: str) -> None:
    """Ajouter des films à la collection movies à partir d'un fichier CSV

    Args:
        fichier (str): chemin vers le fichier CSV à utiiser
    """
    with open(fichier, "r", encoding="utf-8") as f:
        movie_data = csv.DictReader(f)
        # Afficher un spiner pendant que les données sont ajoutées à MongoDB
        spinner = MoonSpinner("adding movies from CSV to the database ")
        state = "LOADING"
        while state != "FINISHED":
            for row in movie_data:
                # Créer une list avec acteurs du film
                row_cast = row["Cast"].split("|")
                movie = Movie(
                    title=row["Title"],
                    year=int(row["Year"]),
                    summary=row["Summary"],
                    short_summary=row["Short Summary"],
                    imdb_id=row["IMDB ID"],
                    runtime=int(row["Runtime"]),
                    trailer=row["YouTube Trailer"],
                    rating=float(row["Rating"]),
                    url_poster=row["Movie Poster"],
                    director=row["Director"],
                    writers=[row["Writers"]],
                    cast=row_cast,
                )
                # Si le film existe déjà dans la base de données, ne l'ajoute
                # pas une 2e fois
                if not movie.in_database():
                    movie.add_to_collection()
                # Tourne le spinner qui montre que les données sont en train
                # d'être ajoutés
                spinner.next()
            # arrêter le spinner quand tous les films sont ajoutés
            state = "FINISHED"
            print("\nUpdate Complete.")


#### Appelez les fonctions quand le programme se lance et import le fichier
#### pour assurer que la collection et la vue sont créés et le validator est en place
create_movies_collection()
add_validator("movies", movies_validator)
create_unique_index("movies", "imdb_id")
create_directors_view()
