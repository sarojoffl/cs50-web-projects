from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from .models import User, Listing

def index(request):
    active_listings = Listing.objects.filter(active=True).order_by('-id')
    return render(request, 'auctions/index.html', {'active_listings': active_listings})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('starting_bid')
        image_url = request.POST.get('image_url')
        category = request.POST.get('category')

        if not title or not description or not starting_bid:
            context = {
                'error': 'Please fill out all required fields.',
                'title': title,
                'description': description,
                'starting_bid': starting_bid,
                'image_url': image_url,
                'category': category,
            }
            return render(request, 'auctions/create_listing.html', context)

        try:
            listing = Listing(
                title=title,
                description=description,
                starting_bid=starting_bid,
                image_url=image_url,
                category=category,
                creator=request.user,
            )
            listing.save()
            return redirect('index')
        except Exception as e:
            context = {'error': f'An error occurred when creating the listing: {e}'}
            return render(request, 'auctions/create_listing.html', context)

    else:
        return render(request, 'auctions/create_listing.html')

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'auctions/listing_detail.html', {'listing': listing})

def category_view(request, category_name):
    listings = Listing.objects.filter(category=category_name, active=True)
    return render(request, 'auctions/category_listings.html', {'listings': listings, 'category_name': category_name})

def category_list(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()
    return render(request, 'auctions/category_list.html', {'categories': categories})

@login_required
def view_watchlist(request):
    user_watchlist = request.user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {'watchlist': user_watchlist})

@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)
    return redirect('listing_detail', listing_id=listing_id)