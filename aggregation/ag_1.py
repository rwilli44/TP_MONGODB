# Local Imports
from models.mongodb import MongoDB


# Lister les 5 réalisateurs les mieux notés


def top_5_directors():
    """Print des 5 réalisateurs les mieux notés et leurs notes."""
    connection = MongoDB()
    db = connection.get_DB()
    pipeline = [
        {
            "$group": {
                "_id": "$director",
                # calculer le moyen des notes
                "average_rating_original": {"$avg": "$rating"},
            }
        },
        # trier par ordre descendant
        {"$sort": {"average_rating_original": -1}},
        {"$limit": 5},
        {
            "$project": {
                "_id": 1,
                # aroundir le moyen des notes à deux places
                "average_rating": {"$round": ["$average_rating_original", 2]},
            }
        },
    ]

    # Print les résultats
    print("\nThe 5 directors with the highest average movie ratings are: \n")

    # Variable pour afficher le classement
    position = 1
    for director in db.movies.aggregate(pipeline):
        print(
            f"{position}: {director.get('_id')} with an average rating of {director.get('average_rating')}."
        )
        position += 1
