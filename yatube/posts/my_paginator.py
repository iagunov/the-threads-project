from django.core.paginator import Paginator
from django.conf import settings


def paginate_queryset(post_list, request):
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
