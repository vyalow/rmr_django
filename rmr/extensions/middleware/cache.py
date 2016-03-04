from django.middleware import cache
from django.utils.cache import patch_cache_control
from django.utils.http import parse_http_date
from django.utils.timezone import now

from rmr.utils.patch import patch


class UpdateCacheMiddleware(cache.UpdateCacheMiddleware):
    """
    Do the same as the original one but try first to use 'key_prefix' from
    the request where it might be saved earlier

    see https://code.djangoproject.com/ticket/15855
    """

    def process_response(self, request, response):
        if 'Expires' in response:
            # Replace 'max-age' value of 'Cache-Control' header by one
            # calculated from the 'Expires' header's date.
            # This is necessary because of Django's `FetchFromCacheMiddleware`
            # gets 'Cache-Control' header from the cache
            # where 'max-age' corresponds to the moment original response
            # was generated and thus may be already stale for the current time
            expires = parse_http_date(response['Expires'])
            timeout = expires - int(now().timestamp())
            patch_cache_control(response, max_age=timeout)

        key_prefix = getattr(request, '_cache_key_prefix', self.key_prefix)
        with patch(self, 'key_prefix', key_prefix):
            return super().process_response(request, response)


class CacheMiddleware(cache.CacheMiddleware):
    """
    Despite of the original one this middleware supports callable 'key_prefix'
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if callable(self.key_prefix):
            self.key_function = self.key_prefix

    def key_function(self, request, *args, **kwargs):
        return self.key_prefix

    def get_key_prefix(self, request):
        key_prefix = self.key_function(
            request,
            *request.resolver_match.args,
            **request.resolver_match.kwargs
        )
        if key_prefix is not None:
            key_prefix = str(key_prefix).replace(' ', '_')
        return key_prefix

    def process_request(self, request):
        self.key_prefix = self.get_key_prefix(request)
        return super().process_request(request)

    def process_response(self, request, response):
        request._cache_key_prefix = self.get_key_prefix(request)

        # you must add rmr's UpdateCacheMiddleware at the top of the
        # MIDDLEWARE_CLASSES to be able to save responses in the cache
        # see https://code.djangoproject.com/ticket/15855
        return response
