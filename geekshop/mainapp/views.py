from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from django.conf import settings
from django.core.cache import cache

import json
import os

from django.views.generic import DetailView

from mainapp.models import Product, ProductCategory

MODULE_DIR = os.path.dirname(__file__)

def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key,link_category)
        return link_category
    else:
        return ProductCategory.objects.all()
# Create your views here.

def index(request):
    context = {
        'title': 'Geekshop', }
    return render(request, 'mainapp/index.html', context)


def products(request,id_category=None,page=1):

    context = {
        'title': 'Geekshop | Каталог',
    }

    if id_category:
        products= Product.objects.filter(category_id=id_category).select_related('category')
    else:
        products = Product.objects.all().select_related('category')

    paginator = Paginator(products,per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)


    context['products'] = products_paginator
    # context['categories'] = ProductCategory.objects.all()
    context['categories'] = get_link_category()
    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    """
    Контроллер вывода информации о продукте
    """
    model = Product
    template_name = 'mainapp/detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(ProductDetail, self).get_context_data(**kwargs)
    #     product = self.get_object()
    #     context['product'] = product
    #     return context

