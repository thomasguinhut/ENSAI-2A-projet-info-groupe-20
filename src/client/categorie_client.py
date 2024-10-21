import requests

from typing import List


class CategorieClient:
    """Make call to the pokemon endpoint"""

    def __init__(self) -> None:
        pass

    def get_categorie(self) -> List[dict]:

        # Appel du Web service
        req = requests.get("https://www.themealdb.com/api/json/v1/1/categories.php?")
        liste_categories = []
        if req.status_code == 200:
            raw_types = req.json()["categories"]
            for t in raw_types:
                categorie = {}
                categorie["id_categorie"] = t["idCategory"]
                categorie["nom_categorie"] = t["strCategory"]
                liste_categories.append(categorie)

        return liste_categories
