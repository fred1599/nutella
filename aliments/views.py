from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from aliments.models import Aliment
from .utils import (
    get_product_by_name,
    get_substitutes,
    wrap_list,
)

from django.conf import settings

@csrf_exempt
def product_view(request, page_number):
    """
    Affichage des produits des mêmes catégories
    :param page_number: page de la vue actuelle
    """
    if page_number == 1 and request.POST:
        if 'product' not in request.POST:
            return redirect('index')
        query = request.POST['product']  # Récupération de la query utilisateur
        if not query:
            return redirect('index')  # Si l'utilisateur envoi une recherche vide
        request.session['product'] = get_product_by_name(query)  # Recherche sur open food facts le nom du produit
        # Enregistrement du résultat pour la session actuelle
        request.session['substitutes'] = wrap_list(get_substitutes(request.session['product']), 6)
        # Recherche et enregistrement du substitut pour la session actuelle

    if page_number >= 1:
        if 'product' not in request.session and 'substitutes' not in request.session:
            return redirect('index')
        product = request.session['product']
        substitutes = request.session['substitutes']
        try:
            sub_page = substitutes[page_number - 1]  # renvoi les substituts de la page numérotée
        except IndexError:
            return redirect('index')

        return render(
            request, 'aliments/base.html', {
                'p': product, 's': sub_page,
                'user': request.user, 'page_suivant': str(int(page_number) + 1),
                'page_precedent': int(page_number) - 1,
            }
        )
    return redirect('index')


def save_view(request, product):
    """
    Si product n'existe pas dans la base, on crée l'aliment
    On sauvegarde dans les favoris de l'utilisateur l'aliment
    :param product: Nom du produit
    """

    # Récupération du substitut du produit
    if request.POST:
        substitutes = request.session['substitutes']
        substitute = None
        for sub in substitutes:
            for s in sub:
                try:
                    if s['product_name_fr'] == product:
                        substitute = s
                        break
                except KeyError:
                    continue

        if substitute:
            # Si le substitut n'est pas dans la base
            aliment = Aliment.objects.filter(user_set=request.user, name=substitute['product_name_fr'])
            if not aliment:
                aliment = Aliment.objects.create(
                    name=substitute['product_name_fr'],
                    url=substitute['url'],
                    url_image=substitute['image_small_url'],
                    score=substitute['nutrition_grades_tags'][0],
                )
                aliment.user_set.add(request.user)  # on ajoute l'utilisateur pour l'aliment favoris
                aliment.save()
    return redirect('/account/profil#section')


@csrf_exempt
def save(request):
    """
    Récupération de l'ensemble des produits cochés et ajout dans les favoris
    Requête ajax
    """
    if request.POST:
        res = request.POST.getlist('results[]')  # voir template base.html pour voir la requête ajax
        for value in res:
            # pour éviter des appels supplémentaires de get_product_by_name
            # petit hack dans le template
            name, url, score, url_image = value.split(';')
            # Mieux qu'un appel à get qui renvoie une exception dans le cas d'aliment introuvable
            # filter renvoi un QuerySet vide, test devient simple
            aliment = Aliment.objects.filter(name=name, url=url, score=score).last()
            if not aliment:
                aliment = Aliment.objects.create(name=name, url=url, score=score, url_image=url_image)
            try:
                aliment = Aliment.objects.get(user_set=request.user, url=url)
            except Aliment.DoesNotExists:
                aliment.user_set.add(request.user)
                aliment.save()

    return redirect('index') if not request.POST else render(request, 'account/profil.html', {})


def delete(request, product):
    """
    Vue pour supprimer un produit en particulier
    :param product: Nom du produit à supprimer
    """
    if request.POST:
        Aliment.objects.get(user_set=request.user, name=product).delete()
        return redirect('/account/profil#section')
    return redirect('index')


def display(request):
    """
    Vue affichant tous les favoris (aliments) de l'utilisateur
    """
    if request.user.is_authenticated:
        aliments = Aliment.objects.filter(user_set=request.user)
        return render(request, 'aliments/food.html', {'aliments': aliments})
    return redirect('index')


def detail_view(request, name_product):
    """
    Vue des détails d'un produit
    :param name_product: Nom du produit dont on souhaite les détails
    """
    substitutes = request.session['substitutes']
    infos = ('product_name_fr', 'categories', 'nutrition_grades_tags', 'image_small_url', 'ingredients_text_fr', 'url')
    res = []
    for list_s in substitutes:
        for s in list_s:
            if s['product_name_fr'] == name_product:
                for info in infos:
                    if info == 'nutrition_grades_tags':
                        val = s[info][0]
                    else:
                        val = s[info]
                    res.append(val)
                return render(request, 'aliments/details.html', {'product': res})
    return redirect('index')

def handle_request(request):
    settings.client.user_context({
        'email': request.user.email
    })
