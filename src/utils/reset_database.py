import os
import dotenv

from utils.singleton import Singleton
from dao.db_connection import DBConnection

from service.joueur_service import JoueurService


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def lancer(self):
        print("Réinitialisation de la base de données")

        dotenv.load_dotenv()

        schema = os.environ["SCHEMA"]
        create_schema = (
            f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"
        )

        init_db = open("data/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        init_db.close()

        pop_db = open("data/pop_db.sql", encoding="utf-8")
        pop_db_as_string = pop_db.read()
        pop_db.close()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
                    cursor.execute(pop_db_as_string)
        except Exception as e:
            print(e)
            raise

        joueur_service = JoueurService()
        for j in joueur_service.lister_tous():
            joueur_service.modifier(j)

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
