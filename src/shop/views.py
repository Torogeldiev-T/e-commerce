from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender
from . documents import ProductDocument
from elasticsearch_dsl.query import Q, MoreLikeThis
from elasticsearch_dsl.search import Search


def product_list(request, category_slug=None):
    if request.method == 'GET':
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return render(request,
                      'shop/product/list.html',
                      {'category': category,
                       'categories': categories,
                       'products': products})
    else:
        search_data = request.POST['search']
        print(search_data)
        results = ProductDocument.search().query
        results = results("match", name=search_data) or results(
            "match", description=search_data)
        results = results.to_queryset()
        categories = Category.objects.all()
        return render(request,
                      'shop/product/list.html',
                      {
                          'categories': categories,
                          'results': results})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})


# When users log in to the site, their anonymous session is lost and
# a new session is created for authenticated users. If you store items
# in an anonymous session that you need to keep after the user logs
# in, you will have to copy the old session data into the new session.
# You can do this by retrieving the session data before you log in
# the user using the login() function of the Django authentication
# system and storing it in the session after that.
