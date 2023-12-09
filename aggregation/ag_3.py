# Local Imports
from models.mongodb import MongoDB


# Les 5 réalisateurs ayant le plus de films


def most_prolific_directors() -> None:
    """Print les 5 réalisateurs qui ont le plus de films dans
    la collection avec le nombre de films pour chacun.
    """

    connection = MongoDB()
    db = connection.get_DB()
    pipeline: list[dict] = [
        {
            "$group": {
                "_id": "$director",
                "total_films": {"$count": {}},
            }
        },
        {"$sort": {"total_films": -1}},  # ordre descendant
        {"$limit": 5},
    ]

    # Print les résultats
    print("\nThe 5 directors with the most films are: \n")
    # Variable pour afficher le classement
    rank: int = 1
    for director in db.movies.aggregate(pipeline):
        print(
            f"{rank}: {director.get('_id')} with a total of {director.get('total_films')} films."
        )
        rank += 1
