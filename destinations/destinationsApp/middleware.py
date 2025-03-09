from django.http import HttpRequest, HttpResponse

from .models import Session, User


def session_middleware(next):

    def middleware(req: HttpRequest) -> HttpResponse:
        token = req.COOKIES.get('token')
        session = None
        if token is not None and Session.objects.filter(token=token).exists():
            session = Session.objects.get(token=token)
            req.user = session.User.id
        res = next(req)
        return res

    return middleware
