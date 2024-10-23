import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection
from business_object.ingredient import Ingredient
from business_object.utilisateur import Utilisateur
from business_object.recette import Recette


class ListeCourseDao(metaclass=Singleton):

    """

    Création de la classe ListeCourseDao.

    Cette classe fait le lien entre les objets des classes métiers
    et la table liste_course de la base de données.

    """

    @log
    def supprimer(self, ingredient: Ingredient) -> bool:
        """

        Suppression un ingrédient donné de la liste de courses
        dans la base de données

        Parameters
        ----------
        ingredient : Ingredient
            ingredient à supprimer de la liste de courses

        Returns
        -------
            True si l'ingredient a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer l'ingrédient de la liste de courses'
                    cursor.execute(
                        "DELETE FROM liste_course                  "
                        " WHERE id_ingredient=%(id_ingredient)s      ",
                        {"id_ingredient": ingredient.id_ingredient},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def trouver_par_id(self, utilisateur: Utilisateur,
                       ingredient: Ingredient) -> bool:
        """

        Determiner si un couplage (utilisateur, ingrédient) donné existe dans
        la liste de courses.

        Parameters
        ----------
        utilisateur : Utilisateur
        ingredient : Ingredient

        Returns
        -------
         True si ce couplage existe déjà et False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM liste_course                      "
                        " WHERE id_utilisateur = %(id_utilisateur)s "
                        " AND id_ingredient = %(id_ingredient)s;  "
                    )

                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        return res is not None

    @log
    def ajouter_recette_a_liste(self, utilisateur: Utilisateur,
                                recette: Recette) -> bool:
        """

        Ajout de tous les ingrédients d'une recette à la liste de courses
        d'un utilisateur donné.

        Parameters
        ----------
        utilisateur : Utilisateur
        recette : Recette

        Returns
        -------
        created : bool
            True si l'ajout est un succès, False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Récupération des ingrédients de la recette
                    cursor.execute(
                        """
                        SELECT i.id_ingredient
                        FROM ingredient i
                        JOIN recette_ingredient ri
                            ON i.id_ingredient = ri.id_ingredient
                        WHERE ri.id_recette = %(id_recette)s
                        """,
                        {
                            "id_recette": recette.id_recette,
                        }
                    )
                    ingredients = cursor.fetchall()

                    # Ajout des ingrédients à la liste de courses
                    for ingredient in ingredients:
                        id_ingredient = ingredient["id_ingredient"]
                        # Vérification si l'ingrédient est déjà dans la liste
                        # de courses
                        cursor.execute(
                            "SELECT 1 FROM liste_course"
                            "WHERE id_utilisateur=% (id_utilisateur)s "
                            "AND id_ingredient = %(id_ingredient)s",
                            {
                                "id_utilisateur": utilisateur.id_utilisateur,
                                "id_ingredient": id_ingredient,
                            }
                        )
                        if not cursor.fetchone():
                            cursor.execute(
                                "INSERT INTO liste_course(id_utilisateur,"
                                "id_ingredient) VALUES"
                                "(%(id_utilisateur)s, %(id_ingredient)s)",
                                {
                                    "id_utilisateur": (
                                        utilisateur.id_utilisateur),
                                    "id_ingredient": id_ingredient,
                                }
                            )

            return True  # Tous les ingrédients ont été ajoutés avec succès

        except Exception as e:
            logging.info(e)
            return False  # En cas d'erreur

    @log
    def lister_ingredients_liste_course(
        self,
        utilisateur: Utilisateur
    ) -> list[Ingredient]:
        """

        Liste tous les ingrédients de la liste de course de l'utilisateur.

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        liste_ingredients : list[Ingredient]
            renvoie la liste de tous les ingrédients de la liste de course
            de l'utilisateur
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "  SELECT *                              "
                        "  FROM ingredient  "
                        "  JOIN liste_course USING (id_ingredient)        "
                        "  WHERE id_utilisateur = %(id_utilisateur)s;    "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_ingredients = []

        if res:
            for row in res:
                ingredient = Ingredient(
                    id_ingredient=row["id_ingredient"],
                    nom_ingredient=row["nom_ingredient"],
                )

                liste_ingredients.append(ingredient)

        return liste_ingredients
