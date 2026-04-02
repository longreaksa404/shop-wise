from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProductPagination(PageNumberPagination):
    page_size = 10 # each page show 10 items
    page_size_query_param = 'page_size' # let frontend override pages if they want Show per page: [10] [25] [50]
    max_page_size = 100  #  but not beyond 100

    def get_paginated_response(self, data):
        return Response({
            'message': 'success',
            'pagination': {
                'total': self.page.paginator.count, # count all product   
                'page': self.page.number, # current page
                'page_size': self.get_page_size(self.request), # items per page
                'total_pages': self.page.paginator.num_pages, # how many pages exist in total frontend easy to know when to disable next button
                'next': self.get_next_link(), # urls to the next page
                'previous': self.get_previous_link(),
            },
            'data': data,
        })