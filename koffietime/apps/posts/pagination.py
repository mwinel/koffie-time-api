from rest_framework.pagination import PageNumberPagination


class PostsPagination(PageNumberPagination):
    # This Django pagination style accepts a single
    # page number in the request parameter.
    page_size = 25
    page_size_query_param = 'page_size'


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
