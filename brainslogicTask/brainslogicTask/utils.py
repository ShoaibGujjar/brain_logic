from django.http import HttpResponseForbidden
import time
from django.conf import settings
from brainslogicTask.settings import r
def ratelimit_request(key_prefix, limit, expire_time):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Get the IP address of the client
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            
            # Generate a unique Redis key for the IP address
            key = f'{key_prefix}:{ip_address}'
            
            # Get the current count for this IP address
            count = r.get(key)
            if count is None:
                count = 0
            else:
                count = int(count)
            
            # If the count exceeds the limit, return a forbidden response
            if count >= limit:
                return HttpResponseForbidden('Too many requests from this IP address.')
            
            # Increment the count and set the expiry time
            r.incr(key)
            r.expire(key, expire_time)
            
            # Call the view function
            return view_func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator
