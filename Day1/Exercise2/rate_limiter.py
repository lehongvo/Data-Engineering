from functools import wraps
from flask import request, jsonify
import time
from collections import defaultdict
import threading


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()

    def _cleanup_old_requests(self, ip, window):
        """Remove requests older than the window"""
        current_time = time.time()
        with self.lock:
            self.requests[ip] = [
                req_time
                for req_time in self.requests[ip]
                if current_time - req_time < window
            ]

    def check_rate_limit(self, ip, limit, window):
        """Check if the request should be rate limited"""
        self._cleanup_old_requests(ip, window)

        with self.lock:
            if len(self.requests[ip]) >= limit:
                return False

            self.requests[ip].append(time.time())
            return True


# Global rate limiter instance
limiter = RateLimiter()


def rate_limit(limit=100, window=60):
    """
    Rate limiting decorator

    Args:
        limit (int): Maximum number of requests allowed within the window
        window (int): Time window in seconds
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr

            if not limiter.check_rate_limit(ip, limit, window):
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": f"Rate limit exceeded. Maximum {limit} requests per {window} seconds.",
                        }
                    ),
                    429,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator
