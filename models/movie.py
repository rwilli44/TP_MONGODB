# Standard Library Imports
import pprint

# Local Imports
from models.mongodb import MongoDB


class Movie:
    def __init__(
        self,
        title: str,
        year: int,
        summary: str,
        short_summary: str,
        imdb_id: str,
        runtime: int,
        trailer: str,
        rating: float,
        url_poster: str,
        director: str,
        **kwargs,
    ) -> None:
        self.title = title
        self.year = year
        self.summary = summary
        self.short_summary = short_summary
        self.imdb_id = imdb_id
        self.runtime = runtime
        self.rating = rating
        self.url_poster = url_poster
        self.director = director
        for key in kwargs:
            # if a value of None is passed in from csv or user, ignore it
            if kwargs[key] == None or len(kwargs[key]) == 0:
                break
            # if a list of writers is given, set it
            if key == "writers":
                self.writers = kwargs[key]
            elif key == "cast":
                self.cast = kwargs[key]
            elif key == "trailer":
                self.trailer = trailer

    def add_to_collection(self):
        connection = MongoDB()
        db = connection.get_DB()
        db.movies.insert_one(self.__dict__)

    def show_movie(self):
        print(self.__dict__)

    def in_database(self):
        connection = MongoDB()
        db = connection.get_DB()
        if db.movies.find_one({"title": self.title, "year": self.year}):
            return True
        else:
            return False

    #### SETTERS

    @classmethod
    def add_new_movie(cls):
        title = input("\nPlease enter the title : ").title()
        year = input("\nPlease enter the year the film was released : ")
        try:
            year = int(year)
        except:
            print(
                f"The year must be a four-digit number. Please start over and try again."
            )
            return None
        summary = input("\nPlease enter a complete summary : \n")
        short_summary = input("\nPlease enter a short summary : \n")
        imdb_id = input(
            "\nPlease enter the year the IMDB ID.\n This should be 9 alphanumeric characters : "
        )
        trailer = input("\nPlease enter the Youtube Trailer ID: ")
        runtime = input(
            "\nPlease enter the runtime of the film in minutes as a whole number: "
        )
        try:
            runtime = int(runtime)
        except:
            print(f"Runtime must be a whole number. Please start over and try again.")
            return None
        rating = input("\nPlease enter the average viewer rating for the film : ")
        try:
            rating = float(rating)
        except:
            print(f"Not a valid rating. Please start over and try again.")
            return None
        url_poster = input(
            "\nPlease enter the complete URL for the film poster. \nThis should begin with 'https://' and end with '.jpg'.\n URL : "
        )
        director = input("\nPlease enter the director's full name : \n")
        writers = input(
            "\nPlease enter the full name(s) of the writer(s). Seperate muliple writers with a comma.\n Writers: "
        ).title()
        writers = writers.split(",")
        cast = input(
            "\nPlease enter the full names of the cast members. Seperate muliple actors with a comma.\n Cast: "
        ).title()
        cast = cast.split(",")
        movie = Movie(
            title=title,
            year=year,
            summary=summary,
            short_summary=short_summary,
            imdb_id=imdb_id,
            runtime=runtime,
            trailer=trailer,
            rating=rating,
            url_poster=url_poster,
            director=director,
            writers=writers,
            cast=cast,
        )
        pprint.pprint(movie.__dict__)
        confirmation = input(
            "\nIs the above information correct? Press N to cancel or any other key to add the movie to the collection.\n Correct? :"
        )
        if confirmation.lower() != "n" and not movie.in_database():
            try:
                movie.add_to_collection()
                print("\nThe movie was successfully added to the collection.\n")
            except Exception as e:
                print(
                    f"The following error occured. Double check that the IMDB ID is correct and unique.\n{e}"
                )

        elif movie.in_database():
            print(
                f"Sorry, a movie entitled {title} released in {year} already exists in the collection."
            )
        else:
            print("\nThe movie was not added to the collection.\n")
