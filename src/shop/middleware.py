import time
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.conf import settings
from importlib import import_module
from django.contrib.sessions.middleware import SessionMiddleware


class AdminCookieSessionMiddleware(SessionMiddleware):
    def cookie_name(self, request):
        if request.path.startswith(u'/admin'):
            return settings.ADMIN_SESSION_COOKIE_NAME
        return settings.SESSION_COOKIE_NAME

    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.COOKIES.get(self.cookie_name(request), None)
        request.session = engine.SessionStore(session_key)

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
        except AttributeError:
            pass
        else:
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            if modified or settings.SESSION_SAVE_EVERY_REQUEST:
                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = cookie_date(expires_time)
                # Save the session data and refresh the client cookie.
                # Skip session save for 500 responses, refs #3881.
                if response.status_code != 500:
                    request.session.save()
                    response.set_cookie(self.cookie_name(request),
                                        request.session.session_key, max_age=max_age,
                                        expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                                        path=settings.SESSION_COOKIE_PATH,
                                        secure=settings.SESSION_COOKIE_SECURE or None,
                                        httponly=settings.SESSION_COOKIE_HTTPONLY or None)
        return response
