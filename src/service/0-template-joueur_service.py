from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao


class JoueurService:
    """Classe contenant les méthodes de service des Joueurs"""

    @log
    def creer(self, pseudo, mdp, age, mail, fan_pokemon) -> Joueur:
        """Création d'un joueur à partir de ses attributs"""

        nouveau_joueur = Joueur(
            pseudo=pseudo,
            mdp=hash_password(mdp, pseudo),
            age=age,
            mail=mail,
            fan_pokemon=fan_pokemon,
        )

        return nouveau_joueur if JoueurDao().creer(nouveau_joueur) else None

    @log
    def lister_tous(self, inclure_mdp=False) -> list[Joueur]:
        """Lister tous les joueurs
        Si inclure_mdp=True, les mots de passe seront inclus
        Par défaut, tous les mdp des joueurs sont à None
        """
        joueurs = JoueurDao().lister_tous()
        if not inclure_mdp:
            for j in joueurs:
                j.mdp = None
        return joueurs

    @log
    def trouver_par_id(self, id_joueur) -> Joueur:
        """Trouver un joueur à partir de son id"""
        return JoueurDao().trouver_par_id(id_joueur)

    @log
    def modifier(self, joueur) -> Joueur:
        """Modification d'un joueur"""

        joueur.mdp = hash_password(joueur.mdp, joueur.pseudo)
        return joueur if JoueurDao().modifier(joueur) else None

    @log
    def supprimer(self, joueur) -> bool:
        """Supprimer le compte d'un joueur"""
        return JoueurDao().supprimer(joueur)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les joueurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["pseudo", "age", "mail", "est fan de Pokemon"]

        joueurs = JoueurDao().lister_tous()

        for j in joueurs:
            if j.pseudo == "admin":
                joueurs.remove(j)

        joueurs_as_list = [j.as_list() for j in joueurs]

        str_joueurs = "-" * 100
        str_joueurs += "\nListe des joueurs \n"
        str_joueurs += "-" * 100
        str_joueurs += "\n"
        str_joueurs += tabulate(
            tabular_data=joueurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_joueurs += "\n"

        return str_joueurs

    @log
    def se_connecter(self, id_utilisateur, mdp) -> Utilisateur:
        """Se connecter à partir de pseudo et mdp"""
        return UtilisateurDao().se_connecter(, hash_password(mdp, pseudo))

    @log
    def identifiant_deja_utilise(self, id_utilisateur) -> bool:
        """Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"""
        utilisateurs = UtilisateurDao().lister_tous()
        return id in [u.id_utilisateur for u in utilisateurs]
