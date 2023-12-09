# Standard Library Imports
import pprint

# Third-Party Imports
from pymongo.database import Database

# Local Imports
from models.mongodb import MongoDB
from models.movie import Movie


class Director:
    """Class pour intéragir avec la vue 'directors" dans laquelle les films
    sont organisés par réalisateur. _id de la vue est le nom de réalisateur."""

    def __init__(self, name: str, movies: list[Movie]) -> None:
        self.name = name
        self.movies = movies

    @classmethod
    def show_films(cls) -> None:
        """Méthode de classe pour chercher les films par le nom de directeur. Print
        le nom de directeur trouvé et une liste des détails de ses films.
        """

        search_name: str = input("Director's name : ")
        query: dict = {"_id": {"$regex": search_name, "$options": "i"}}
        projection: dict = {"_id": 1, "movies": 1}
        results_found: int = 0
        connection: MongoDB = MongoDB()
        db: Database = connection.get_DB()
        for film in db.directors.find(query, projection):
            results_found += 1
            pprint.pprint(film)  # pprint pour rendre les films plus lisibles
        if results_found == 0:
            print(f"\nSorry, no results were found for {search_name}.\n")

    @classmethod
    def find_avg_rating(cls) -> None:
        """Méthode de classe pour chercher le nom d'un directeur pour afficher la
        note moyenne de ses films. Print la résultat.
        """
        connection: MongoDB = MongoDB()
        db: Database = connection.get_DB()
        search_input: str = input("Director's name : ")
        pipeline: list[dict] = [
            {"$match": {"director": {"$regex": search_input, "$options": "i"}}},
            {
                "$group": {
                    "_id": "$director",
                    "average_rating_complete": {"$avg": "$rating"},
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "average_rating": {"$round": ["$average_rating_complete", 2]},
                }
            },
        ]

        results_found: int = 0
        for director in db.movies.aggregate(pipeline):
            results_found += 1
            print(
                f"The average rating for {director.get('_id')}'s films is {director.get('average_rating')}.\n"
            )
        if results_found == 0:
            print(f"\nSorry, no results were found for {search_input}.\n")
