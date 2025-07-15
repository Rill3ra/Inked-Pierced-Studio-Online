from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Certificate
from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(parent=None)
    products = Product.objects.filter(is_available=True, is_certificate=False) # Исключаем сертификаты по умолчанию
    certificates = Certificate.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(
            category__slug=category_slug, is_certificate=False
        )  # Исключаем сертификаты при фильтрации
    # Обработка фильтров
    material = request.GET.get('material')
    style = request.GET.get('style')

    if material:
        products = products.filter(material=material)
    if style:
        products = products.filter(style=style)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'certificates': certificates, # Передаем сертификаты в любом случае, но они не будут отображаться, если не итерироваться по ним
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product,
                                 category__slug=category_slug,
                                 slug=product_slug,
                                 is_available=True)
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)

def product_search(request):
    query = request.GET.get('q')
    products = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()
    return render(request, 'products/product_list.html', {'products': products, 'query': query})

def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    return render(request, 'products/certificate_detail.html', {'certificate': certificate})

def home(request):
    return render(request, 'home.html')