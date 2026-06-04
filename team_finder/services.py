from django.core.paginator import Paginator


PAGE_SIZE = 12


def get_paginated_page(request, queryset, per_page=PAGE_SIZE):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
