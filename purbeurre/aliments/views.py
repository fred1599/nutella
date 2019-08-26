from django.shortcuts import redirect, render

from aliments.utils import (
    get_product_by_name,
    get_substitute,
)


def product_view(request):
    if request.method != 'POST':
        return redirect('index')

    query = request.POST['product']
    if not query:
        return redirect('index')

    product = get_product_by_name(query)
    substitute = get_substitute(product)
    if substitute:
        return render(request, 'aliments/base.html', {'p': product, 's': substitute})
    return redirect('index')
