from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import customers
from django.shortcuts import redirect

RATE_LIMITS = {
    customers.GOLD_GROUP: '10/minute',
    customers.SILVER_GROUP: '5/minute',
    customers.BRONZE_GROUP: '2/minute',
}

class GroupRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            group = user.group
            rate_limit = RATE_LIMITS.get(group, None)
            if rate_limit:
                # Check if user has exceeded rate limit
                cache_key = f'user:{user.pk}'
                current_time = int(timezone.now().timestamp())
                rate_info = cache.get(cache_key, {'count': 0, 'time': current_time})
                if current_time - rate_info['time'] > 60:
                    rate_info['count'] = 0
                    rate_info['time'] = current_time
                if rate_info['count'] >= (int(rate_limit.split('/')[0])):
                    raise PermissionDenied
                rate_info['count'] += 1
                cache.set(cache_key, rate_info, timeout=60)
        
        # Allow access to the index page only for authenticated users
        if request.path == '/' and not user.is_authenticated:
            return redirect('login')
        
        response = self.get_response(request)
        return response
