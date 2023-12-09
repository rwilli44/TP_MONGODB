# Local Imports
from models.mongodb import MongoDB


# Les 5 réalisateurs dont les films ont la durée moyenne la plus importante


def directors_longest_runtimes():
    """Print des 5 réalisateurs qui ont la plus longue
    durée moyenne pour leurs films"""

    connection = MongoDB()
    db = connection.get_DB()
    pipeline: list[dict] = [
        {
            "$group": {
                "_id": "$director",
                # trouver le moyen de la durée des films du réalisateur
                "average_runtime_complete": {"$avg": "$runtime"},
            }
        },
        # trier par ordre descendant
        {"$sort": {"average_runtime_complete": -1}},
        {"$limit": 5},
        {
            "$project": {
                "_id": 1,
                # aroundir le moyen de la durée des films à deux places
                "average_runtime": {"$round": ["$average_runtime_complete", 2]},
            }
        },
    ]

    # Print les résultats
    print("\nThe 5 directors with the longest average runtime are: \n")

    # Variable pour afficher le classement
    rank = 1
    for director in db.movies.aggregate(pipeline):
        print(
            f"{rank}: {director.get('_id')} with an average runtime of {director.get('average_runtime')}."
        )
        rank += 1
