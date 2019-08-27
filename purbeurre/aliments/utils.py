from random import choice, shuffle

import requests

import logging

logger = logging.getLogger(__name__)


def check_common_categories(p1, p2):
    """
    p1 et p2 sont des produits où l'on souhaite vérifier qu'ils ont des catégories en commun
    évite les recherches pouvant être faussées.
    p1 et p2 sont des dictionnaires
    Retourne les catégories en commun
    :param p1: produit 1
    :param p2: produit 2
    :type p1: dict résultant de json['products'][indice]
    :type p2: dict
    :return: Retourne les catégories en commun (type set)
    """

    try:
        if p1['product_name_fr'] != p2['product_name_fr']:
            if p1['nutrition_grades_tags'][0] != p2['nutrition_grades_tags'][0]:

                cat_1 = p1.get('categories', None).strip()  # on récupère les catégories du produit
                cat_2 = p2.get('categories', None).strip()  # elles sont de type str

                if cat_1 and cat_2:
                    cat_1_list = map(str.strip, cat_1.split(','))  # chaîne séparée par des virgules c'est très moche pour une API
                    cat_2_list = map(str.strip, cat_2.split(','))

                    return set(cat_1_list) & set(cat_2_list)  # il est possible qu'aucune catégorie soit en commun: set vide
        return set()  # pas de catégories en commun on passera à la comparaison du produit suivant
    except KeyError:
        return set()


def get_common_max_categories(p1, products):
    """
    p1 est le produit où l'on souhaitera récupérer un substitut avec le maximum de catégories en commun
    :param p1: dictionnaire avec toutes les infos nécessaires au produit
    :param products: Ensemble des produits d'une catégorie demandée (déduite d'une catégorie de p1)
    :return: retourne le produit ayant le maximum de catégories en commun
    """
    product = p1
    shuffle(products)  # on mélange les produits pour ne pas tomber sur toujours le même
    length_common = 0
    for p in products:
        common_categories = check_common_categories(p1, p)
        if common_categories and (len(common_categories) > length_common):
            length_common = len(common_categories)
            product = p

    return product


def get_product_by_name(name):
    """
    :param name: nom du produit recherché
    :return: le produit avec toutes ses infos
    :return type: dict
    """

    if name:
        name = name.strip().lower()
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


def get_substitute(p1):
    """
    Retourne le substitut du produit p1 si son score est meilleur et qu'il en existe un.
    :param p1: produit dont on cherche le substitut
    :return: retourne le produit représentant le substitut
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
        return p1  # Pas de substitut possible alors on retourne le produit d'origine

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

    good = False
    while not good:
        if not products:
            good = True
            logger.info('Pas de meilleur substitut pour le score')
            continue

        product = get_common_max_categories(p1, products)  # produit avec le maximum de catégories en commun avec p1

        score_grade_substitut = product['nutrition_grades_tags'][0]  # on vérifie le score du substitut
        if len(score_grade_substitut) == 1:  # si le score est valide, API pourrie, pourquoi pas une liste vide ?
            score_grade_p1 = p1['nutrition_grades_tags'][0]
            if len(score_grade_p1) == 1:
                logger.info('Les scores sont comparables')
                if ord(score_grade_p1) > ord(score_grade_substitut):
                    return product

        if product in products:
            products.remove(product)

        else:
            good = True

    return p1  # soit le score n'est pas comparable, soit le score est supérieur à celui du produit à substituer
