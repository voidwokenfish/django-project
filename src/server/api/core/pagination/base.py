from rest_framework.pagination import PageNumberPagination


class StandardPagePagination(PageNumberPagination):
    """Переопределение класса пагинации респонса."""

    page_size = 20
    page_size_query_param = 'count'
