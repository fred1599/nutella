from random import choice
from string import punctuation

from aliments.models import Aliment, Favoris

import requests

import logging

logger = logging.getLogger(__name__)


def get_product_by_name(name):
    """
    :param name: nom du produit recherché
    :return: le produit avec toutes ses infos
    :return type: dict
    """

    if name:
        name = name.strip().lower().translate(str.maketrans('', '', punctuation))
        api_url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        params = {
            'search_terms': name,
            'search_simple': '1',
            'action': 'process',
            'sort_by_unique': 'unique_scans_n',
            'page_size': 20,  # on recherche sur une seule page pour limiter le temps d'attente
            'json': 1
        }

        results = requests.get(api_url, params).json()
        if results['products']:
            return choice(results['products'])  # on retourne au hasard un produit de la base
    return {}


def get_substitutes(p1):
    """
    Retourne les substituts possibles du produit p1 si son score est meilleur et qu'il en existe au moins un.
    :param p1: produit dont on cherche le substitut
    :return: retourne les substituts par groupe de 6 pour séparer chaque page.
    """

    if not p1:
        return None

    category = p1.get('categories', None)
    if not category:
        name = p1.get('product_name_fr', None)
        if name:
            logger.warning('Pas de catégorie, pas de substitut pour {}'.format(name))
        else:
            logger.warning('produit non reconnue et sans catégorie')
        return [p1, ]  # Pas de substitut possible alors on retourne le produit d'origine

    category = category.strip().split(',')  # liste des catégories du produit

    products = []
    api_url = "https://fr.openfoodfacts.org/cgi/search.pl?"

    for cat in category:
        params = {
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': cat,
            'action': 'process',
            'sort_by_unique': 'unique_scans_n',
            'page_size': 20,
            'json': 1
        }

        results = requests.get(api_url, params).json()
        products += results['products']  # on ajoute l'ensemble produits pour toutes les catégories du produit cherché

    if not products:
        logger.info('Pas de meilleur substitut pour le score')
        return [p1, ]

    score_grade_p1 = p1['nutrition_grades_tags'][0]
    if len(score_grade_p1) != 1:
        logging.warning('les scores ne sont pas comparables avec {}'.format(score_grade_p1))
        return [p1, ]

    substitutes = []
    for product in products:
        score_grade_substitut = product['nutrition_grades_tags'][0]  # on vérifie le score du substitut
        if len(score_grade_substitut) == 1:  # si le score est valide, API pourrie, pourquoi pas une liste vide ?
            if ord(score_grade_p1) > ord(score_grade_substitut):
                substitutes.append(product)

    return substitutes  # retourne liste de produits


def add_product_favorite(product):
    try:
        #  On vérifie si le produit n'est pas dans les favoris
        favourite = Favoris.objects.get(
            user=product.user, aliment_set__name=product.name, aliment_set__url=product.url
        )
    except Favoris.DoesNotExist:
        #  S'il n'existe pas, on ajoute le produit dans les favoris
        Favoris.aliment_set.add(product)


def wrap_list(fruits, step):
    pages = []
    length = len(fruits)
    for i in range(0, length, step+1):
        pages.append(fruits[i:i+step])
    return pages