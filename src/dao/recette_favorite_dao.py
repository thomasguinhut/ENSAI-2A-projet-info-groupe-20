import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection
# from business_object.recette import Recette
# from business_object.utilisateur import Utilisateur


class RecettesFavoritesDao(metaclass=Singleton):
    """Classe contenant les méthodes pour gérer les recettes favorites"""

    @log
    def supprimer(self, recette) -> bool:
        """Suppression d'une recette de la liste des recettes favorites

        Parameters
        ----------
        recette : Recette
            recette à supprimer de la liste des recettes favorites

        Returns
        -------
            True si la recette a bien été supprimée
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer la recette de la liste des recettes favorites
                    cursor.execute(
                        "DELETE FROM recette_favorite                  "
                        " WHERE id_recette=%(id_recette)s      ",
                        {"id_recette": recette.id_recette},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def ajouter_recette_a_liste(self, utilisateur, recette) -> bool:
        """Ajout d'une recette à la liste des recettes favorites d'un utilisateur donné

        Parameters
        ----------
        utilisateur : Utilisateur
        recette : Recette

        Returns
        -------
        created : bool
            True si l'ajout est un succès, False sinon
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO recette_favorite(id_utilisateur, id_recette) VALUES        "
                        "(%(id_utilisateur)s, %(id_recette)s)             "
                        "  RETURNING id_utilisateur;                                ",
                        {"id_utilisateur": utilisateur.id_utilisateur, 
                         "id_recette": recette.id_recette},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise
        created = False
        if res:
            utilisateur.id_utilisateur = res["id_utilisateur"]
            created = True
        return created
        
