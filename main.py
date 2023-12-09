# Standard Library Imports
import random

# Local Imports
from aggregation import ag_1, ag_2, ag_3, ag_4
import load_data
from models.directors import Director
from models.movie import Movie


def random_fact() -> None:
    """Appelez une des fonctionnes d'aggregation, choisi par hasard, pour
    présenter un "fun fact" sur la cinéma à l'utilisateur.
    """

    random_choice: int = random.randint(1, 4)
    match random_choice:
        case 1:
            ag_1.top_5_directors()
        case 2:
            ag_2.directors_longest_runtimes()
        case 3:
            ag_3.most_prolific_directors()
        case 4:
            ag_4.most_prolific_actors()


def main():
    # Demandez à l'utilisateur s'il faut faire l'importation du fichier CSV
    load_csv_choice = input(
        "\n\nWelcome! Would you like to import movies from the default CSV file into the 'movie' collection? Y/N \nResponse: "
    )
    if load_csv_choice.lower() == "y":
        # ajouter les films du csv à la collection de la base de donénes si l'utilisatuer a choisi oui
        load_data.load_movies_from_csv("movies.csv")

    # commencer une boucle pour permettre à l'utilisateur de répéter le choix de plusieurs actions
    while True:
        user_action: str = input(
            """\nMenu: 
            1 - List films by director
            2 - Get the average film rating for a director
            3 - Add a film to the collection 
            4 - See a random fun fact about movies 
            5 - Exit
            
            What would you like to do?  
            Response: """
        )

        match user_action:
            case "1":
                Director.show_films()
            case "2":
                Director.find_avg_rating()
            case "3":
                Movie.add_new_movie()
            case "4":
                random_fact()
            case "5":
                print("\nGoodbye!\n")
                exit()
            # si l'utilisateur choisi autre chose que 1-5, affiche une erreur et récommencer
            case _:
                print("\nInvalid input. Try again.\n")
                continue
        # après l'action choisi, demander si l'utilisateur veut continuer, ceci permet de ne
        # pas afficher immediatement le menu qui peut géner la lecture de la réponse de l'action précédente
        choose_continue = input("\nWould you like to continue? Y/N \nResponse: ")
        if choose_continue.lower() == "y":
            continue
        elif choose_continue.lower() == "n":
            print("\nGoodbye!\n")
            exit()
        else:
            print("\nInvalid input. Returning to main menu.\n")


if __name__ == "__main__":
    main()
