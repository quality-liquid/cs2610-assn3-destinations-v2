from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth.hashers import make_password, check_password
from random import choices
from string import ascii_letters, digits

from .models import Destination, User, Session


def index(req: HttpRequest) -> HttpResponse:
    destinations = Destination.objects.filter(share_publicly=True).order_by('-id')[:5]
    logged_in = 'token' in req.COOKIES # TODO attach this in the middleware
    return render(req, 'destinationsApp/index.html', context={'logged_in': logged_in, 'destinations': destinations})


def new_user(req: HttpRequest) -> HttpResponse:
    return render(req, 'destinationsApp/new_user.html')


def new_session(req: HttpRequest) -> HttpResponse:
    return render(req, 'destinationsApp/new_session.html')


def users(req: HttpRequest) -> HttpResponse:
    name = req.POST.get('name')
    email = req.POST.get('email')
    password = req.POST.get('password')
    if not '@' in email:
        return render(req, 'destinationsApp/new_user.html', context={'bad_email': True})
    elif len(password) < 8 or not any(char.isdigit() for char in password):
        return render(req, 'destinationsApp/new_user.html', context={'bad_password': True})
    else:
        print(password)
        password = make_password(password)
        user = User(name=name, email=email, password_hash=password)
        user.save()
        token = ''.join(choices(ascii_letters + digits, k=20))
        session = Session(User=user, token=token)
        session.save()
        res = redirect('/destinations/')
        res.set_cookie('token', token)
        return res


def sessions(req: HttpRequest) -> HttpResponse:
    email = req.POST.get('email')
    password = req.POST.get('password')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise Http404('No user with given email.')
    if not check_password(password, user.password_hash):
        raise Http404('Password is incorrect.')
    else:
        token = ''.join(choices(ascii_letters + digits, k=20))
        session = Session(User=user, token=token)
        session.save()
        res = redirect('/destinations/')
        res.set_cookie('token', token)
        return res


def destroy_session(req: HttpRequest) -> HttpResponse:
    token = req.COOKIES.get('token')
    if not token:
        raise Http404('No session token found.')
    session = Session.objects.get(token=token)
    session.delete()
    res = redirect('/')
    res.delete_cookie('token')
    return res


def destinations(req: HttpRequest) -> HttpResponse:
    token = req.COOKIES.get('token')
    if not token:
        raise Http404('No session token found.')
    session = Session.objects.get(token=token)
    user = session.User
    if req.method == 'POST':
        dest = req.POST.get('destination')
        review = req.POST.get('review')
        rating = req.POST.get('rating')
        share_publicly = req.POST.get('share_publicly') == 'on'
        new_dest = Destination(User=user, name=dest, review=review, rating=rating, share_publicly=share_publicly)
        new_dest.save()
    destinations = Destination.objects.filter(User=user)
    return render(req, 'destinationsApp/destinations.html', context={'destinations': destinations})


def edit_dest(req: HttpRequest, id: int) -> HttpResponse:
    token = req.COOKIES.get('token')
    if not token:
        raise Http404('No session token found.')
    session = Session.objects.get(token=token)
    user = session.User
    dest = Destination.objects.get(id=id)
    if not user.id == dest.User.id:
        raise Http404('You don\'t own this destination object.')
    elif not dest:
        raise Http404('Destination doesn\'t exist.')
    else:
        if req.method == 'GET':
            id = dest.id
            destination = dest.name
            review = dest.review
            rating = dest.rating
            share = 'y' if dest.share_publicly else 'n'
            return render(req, 'destinationsApp/edit_dest.html', context={'id': id, 'destination': destination, 'review': review, 'rating': rating, 'share': share})
        elif req.method == 'POST':
            dest.name = req.POST.get('destination')
            dest.review = req.POST.get('review')
            dest.rating = req.POST.get('rating')
            dest.share_publicly = req.POST.get('share_publicly') == 'y'
            dest.save()
            return redirect('/destinations/')
            

def destroy_dest(req: HttpRequest, id: int) -> HttpResponse:
    token = req.COOKIES.get('token')
    if not token:
        raise Http404('No session token found.')
    session = Session.objects.get(token=token)
    user = session.User
    dest = Destination.objects.get(id=id)
    if not user.id == dest.User.id:
        raise Http404('You don\'t own this destination object.')
    else:
        dest.delete()
        return redirect('/destinations/')


def new_destination(req: HttpRequest) -> HttpResponse:
    return render(req, 'destinationsApp/new_destination.html')
