from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .utils import (
    get_product_by_name,
    get_substitutes,
    wrap_list,
)

from aliments.models import Aliment


def product_view(request, page_number):
    if page_number == 1 and request.POST:
        if 'product' not in request.POST:
            return redirect('index')
        query = request.POST['product']
        if not query:
            return redirect('index')
        request.session['product'] = get_product_by_name(query)
        request.session['substitutes'] = wrap_list(get_substitutes(request.session['product']), 6)

    if request.POST:
        if 'product' not in request.session and 'substitutes' not in request.session:
            return redirect('index')
        product = request.session['product']
        substitutes = request.session['substitutes']
        try:
            sub_page = substitutes[page_number-1]  # renvoi les substituts de la page numérotée
        except IndexError:
            return redirect('index')

        return render(
            request, 'aliments/base.html', {
                'p': product, 's': sub_page,
                'user': request.user, 'page_suivant':str(int(page_number)+1),
                'page_precedent':int(page_number)-1,
            }
        )
    return redirect('index')


def save_view(request, product):
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
            aliment = Aliment.objects.filter(name=substitute['product_name_fr'])
            if not aliment:
                aliment = Aliment.objects.create(
                    name=substitute['product_name_fr'],
                    url=substitute['url'],
                    url_image=substitute['image_small_url'],
                    score=substitute['nutrition_grades_tags'][0],
                )
                aliment.user_set.add(request.user)
                aliment.save()
    return redirect('profil')


@csrf_exempt
def save(request):
    if request.POST:
        res = request.POST.getlist('results[]')
        for value in res:
            name, url, score, url_image = value.split(';')
            aliment = Aliment.objects.filter(name=name, url=url, score=score)
            if not aliment:
                aliment = Aliment.objects.create(name=name, url=url, score=score, url_image=url_image)
                aliment.user_set.add(request.user)
                aliment.save()

    return redirect('index') if not request.POST else render(request, 'account/profil.html', {})


def delete(request, product):
    if request.POST:
        Aliment.objects.get(name=product).delete()
        return redirect('profil')
    return redirect('index')

def display(request):
    if request.user.is_authenticated:
        aliments = Aliment.objects.all()
        return render(request, 'aliments/food.html', {'aliments': aliments})
    return redirect('index')