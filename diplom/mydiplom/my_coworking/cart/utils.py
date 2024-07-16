from .models import Product
from django.db.models import Q

def search_product(query):
    """
    Функция поиска продуктов по названию.

    Args:
        query (str): Строка, которую пользователь ввел в форму поиска.

    Returns:
        QuerySet: Набор объектов `Product`, соответствующих запросу.
    """
    return Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )