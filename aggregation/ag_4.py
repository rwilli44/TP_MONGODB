# Standard Library Imports
import pprint

# Local Imports
from models.mongodb import MongoDB


# Requête d'agrégation : Le résultat de cette requête doit me donner
# la liste et le nombre de films des 15 acteurs les plus présents


def most_prolific_actors() -> None:
    """Print des 15 acteurs qui ont fait le plus de films en ordre descendant
    avec le nombre de films et une liste de leurs titres.
    """
    connection = MongoDB()
    db = connection.get_DB()

    pipeline: list[dict] = [
        {"$unwind": "$cast"},
        # filtrer les espaces/réponses nulls
        {"$match": {"cast": {"$regex": "[A-Za-z]+", "$options": "i"}}},
        {
            "$group": {
                "_id": "$cast",
                "total_films": {"$count": {}},
                # ajouter une liste des titres des films
                "movies": {"$push": "$title"},
            }
        },
        {"$sort": {"total_films": -1}},
        {"$limit": 15},
    ]

    # Print les résultats
    print("\nThe 15 actors with the most films are: \n")
    # Variable pour afficher le classement
    rank: int = 1
    for actor in db.movies.aggregate(pipeline):
        print(
            f"{rank}: {actor.get('_id')} with a total of {actor.get('total_films')} films:"
        )
        pprint.pprint(actor.get("movies"))  # pprint pour rendre la liste plus lisible
        rank += 1
