from email import message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

from .models import Category, Listing, User, Bid, Comment
from .forms import ListingForm


def index(request):
    all_active_listing = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {"all_active_listing": all_active_listing})


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
            messages.error(
                request, f"Invalid username and/or password.")
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if username == "":
            messages.error(request, f"You need to type your username for registration.")
            return render(request, "auctions/register.html")
        elif email == "":
            messages.error(request, f"You need to type your email address for registration.")
            return render(request, "auctions/register.html")
        elif password == "":
            messages.error(request, f"You need to type your password for registration.")
            return render(request, "auctions/register.html")
        elif confirmation == "":
            messages.error(request, f"You need to type your confirm password for registration.")
            return render(request, "auctions/register.html")

        # Ensure password matches confirmation
        if password != confirmation:
            messages.error(request, f"Passwords must match.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, f"Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def profile_view(request, username):
    user = User.objects.get(username=username)
    user_listing = Listing.objects.filter(owner=user)
    return render(request, "auctions/profile.html", {
        "user": user,
        "user_listing": user_listing
    })


@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save()
            listing.owner = request.user
            listing.start_datetime = timezone.now()
            listing = form.save()
            form = ListingForm()
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })


@login_required(login_url='login')
def edit_listing(request, listing_id):
    target_listing = Listing.objects.get(pk=listing_id)

    if (request.user == target_listing.owner):
        form = ListingForm(request.POST, request.FILES,
                           instance=target_listing)
        if request.method == "POST":
            if form.is_valid():
                listing = form.save()
                messages.success(request, f"Edited sucessfully")
                return render(request, "auctions/listing.html", {
                    "target_listing": target_listing,
                    "watching_by_this_user": request.user.is_watchers(target_listing)
                })

        else:
            form = ListingForm(instance=target_listing)

        return render(request, "auctions/edit_listing.html", {
            "form": form
        })


# Show listing of the category requested by user
# when the user type ...../categories/<categ>
def category(request, categ):
    # Query the category object by 'categ' type by user
    category_object = get_object_or_404(Category, category=categ)
    # Filter the listing object by the category object
    category_listing = Listing.objects.filter(category=category_object)

    return render(request, "auctions/category.html", {
        "category": categ.capitalize(),
        "category_listing": category_listing
    })


# Show all category
def view_all_categories(request):
    # If the user type ...../categories/all => it will show all category
    all_categories = Category.objects.all()
    return render(request, "auctions/all_category.html", {
        "all_categories": all_categories
    })


# listing page
def listing(request, listing_id):
    target_listing = Listing.objects.get(pk=listing_id)
    if request.user.is_anonymous:
        is_watching = False
    else:
        is_watching = request.user.is_watchers(target_listing)

    return render(request, "auctions/listing.html", {
        "target_listing": target_listing,
        "watching_by_this_user": is_watching
    })


# User can make bid after they has login their account
def make_bid(request, listing_id):
    if request.method == "POST":
        target_listing = Listing.objects.get(pk=listing_id)

        # User must login first before make a bid
        if request.user.is_anonymous:
            messages.warning(
                request, f"Sorry, you need to login your account first before make a bid", extra_tags='required_login')
            return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": target_listing.id}))

        # If user did not type anything
        if (request.POST["new_bid"] == ""):
            messages.warning(
                request, f"Dear {request.user}, you need to type a price in order to make bid")
            return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": target_listing.id}))

        new_bid = float(request.POST["new_bid"])
        # Check whether it is within the range
        if (new_bid > target_listing.get_current_bid() and new_bid < 99999.99):
            bid = Bid(auction=target_listing, user=request.user,
                      amount=new_bid, datetime=timezone.now())
            bid.save()

            target_listing.current_bid = new_bid
            target_listing.save()

            messages.success(
                request, f"Dear {request.user}, your bid is sucessfully made!")
            return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": target_listing.id}))

        else:
            messages.warning(
                request, f"Dear {request.user}, you need to type a price that between ${target_listing.current_bid} and $99999.99")
            return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": target_listing.id}))


# User can add or remove the listing from their watchlist in listing page
def edit_watchlist(request, listing_id):
    target_listing = Listing.objects.get(pk=listing_id)

    # User must login first before add to the watchlist
    if request.user.is_anonymous:
        messages.warning(
            request, f"Sorry, you need to login your account first before add to your watchlist", extra_tags='required_login')
        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": target_listing.id}))

    if (request.user.is_watchers(target_listing)):
        target_listing.watchers.remove(request.user)
    else:
        target_listing.watchers.add(request.user)

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": target_listing.id}))


# user can view their own watchlist
@login_required(login_url='login')
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlists.all()
    })


# User can remove the listing from their watchlist
@login_required(login_url='login')
def remove_from_watchlist(request, listing_id):
    target_listing = Listing.objects.get(pk=listing_id)

    if (request.user.is_watchers(target_listing)):
        target_listing.watchers.remove(request.user)

    return HttpResponseRedirect(reverse("watchlist"))


# the owner of the listing can perform deactivate, activate, edit, delete the listing
@login_required(login_url='login')
def listing_owner_setting(request, listing_id):
    target_listing = Listing.objects.get(pk=listing_id)

    if request.POST.get("deactivate", False):
        target_listing.deactivate()

    if request.POST.get("activate", False):
        target_listing.activate()

    target_listing.save()

    if request.POST.get("edit", False):
        return HttpResponseRedirect(reverse("edit_listing", kwargs={"listing_id": target_listing.id}))

    if request.POST.get("delete", False):
        messages.success(
            request, f"Your listing of '{target_listing.title}' already deleted!")
        target_listing.delete()
        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": target_listing.id}))

# Every user can leave their comments to the listing and display on listing page


def leave_comment(request, listing_id):
    if request.method == "POST":
        target_listing = Listing.objects.get(pk=listing_id)

        if request.user.is_anonymous:
            messages.warning(
                request, f"Sorry, you need to login your account first before leave a comment", extra_tags='required_login')
            return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": target_listing.id}))

        comment_content = request.POST["comment-from-user"]
        if comment_content is None or comment_content == "":
            messages.warning(
                request, "You need to type something first before leave a comment!")

        else:
            comment = Comment(auction=target_listing, user=request.user,
                              datetime=timezone.now(), content=comment_content)
            comment.save()
            messages.success(
                request, "You have leave your comment successfully!")

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": target_listing.id}))
