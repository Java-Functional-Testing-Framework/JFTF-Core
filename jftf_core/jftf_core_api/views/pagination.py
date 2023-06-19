from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ContentRangeHeaderPagination(PageNumberPagination):
    page_size_query_param = 'perPage'

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        item_starting_index = self.page.start_index() - 1
        item_ending_index = self.page.end_index() - 1

        content_range = 'items {0}-{1}/{2}'.format(item_starting_index, item_ending_index, total_items)

        headers = {'Content-Range': content_range}

        return Response(data, headers=headers)
