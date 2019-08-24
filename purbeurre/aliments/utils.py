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

    cat_1 = p1.get('categories', None).strip()  # on récupère les catégories du produit
    cat_2 = p2.get('categories', None).strip()  # elles sont de type str

    if cat_1 and cat_2:
        cat_1_list = map(str.strip, cat_1.split(','))  # chaîne séparée par des virgules c'est très moche pour une API
        cat_2_list = map(str.strip, cat_2.split(','))

        return set(cat_1_list) & set(cat_2_list)  # il est possible qu'aucune catégorie soit en commun: set vide

    return set()  # pas de catégories en commun on passera à la comparaison du produit suivant


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
        if p['product_name_fr'].lower() != p1['product_name_fr'].lower():
            common_categories = check_common_categories(p1, p)
            if common_categories and len(common_categories) > length_common:
                length_common = len(common_categories)
                product = p

    return product


def get_product_by_name(name):
    """
    :param name: nom du produit recherché
    :return: le produit avec toutes ses infos
    :return type: dict
    """

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
    return choice(results['products'])  # On choisit un produit au hasard dans la recherche


def get_substitute(p1):
    """
    Retourne le substitut du produit p1 si son score est meilleur et qu'il en existe un.
    :param p1: produit dont on cherche le substitut
    :return: retourne le produit représentant le substitut
    """
    category = p1.get('categories', None).strip().split(',')
    if not category:
        logger.warning('Pas de catégorie, pas de substitut pour {}'.format(p1['product_name_fr']))
        return p1  # Pas de substitut possible

    api_url = "https://fr.openfoodfacts.org/cgi/search.pl?"
    params = {
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': choice(category),
        'action': 'process',
        'sort_by_unique': 'unique_scans_n',
        'page_size': 20,
        'json': 1
    }

    results = requests.get(api_url, params).json()
    products = results['products']
    product = get_common_max_categories(p1, products)  # produit avec le maximum de catégories en commun avec p1
    if not product:
        logger.warning('Pas de produit avec au moins une catégorie en commun')
        return p1

    score_grade_substitut = product['nutrition_grades_tags'][0]  # on vérifie le score du substitut
    if len(score_grade_substitut) == 1:  # si le score est valide, API pourrie, pourquoi pas une liste vide ?
        score_grade_p1 = p1['nutrition_grades_tags'][0]
        if len(score_grade_p1) == 1:
            if ord(score_grade_p1) > ord(score_grade_substitut):
                return product
    logger.warning('Pas de meilleur substitut pour le score, ou impossible de comparer les scores')
    return p1  # soit le score n'est pas comparable, soit le score est supérieur à celui du produit à substituer
