# Third-Party Imports
from pymongo import MongoClient
from pymongo.database import Database


class SingletonMeta(type):
    """
    Metaclasse pour créer les classes Singleton qui donnent le même objet à chaque
    instanciation.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MongoDB(metaclass=SingletonMeta):
    """Tentative de classe type 'Singleton' pour créer l'accès à la base de données.
    Je vois l'idée de ce design pattern mais le façon correcte de l'utiliser reste
    plutôt mystérieux."""

    @classmethod
    def get_DB(cls) -> Database:
        """Retourne un objet d'accès à la base de données MongoDB pour permettre à faire des
        requêtes et aggregations.

        Returns:
            Database: l'objet d'accès à la base de données cinéma
        """
        client: MongoClient = MongoClient("mongodb://localhost:27017/")
        db: Database = client["cinema"]
        return db
