from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>/profile", views.profile_view, name="view_profile"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories/all", views.view_all_categories, name="view_all_categories"),
    path("categories/<str:categ>", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/make_bid", views.make_bid, name="make_bid"),
    path("listing/<int:listing_id>/owner_setting", views.listing_owner_setting, name="owner_setting"),
    path("listing/<int:listing_id>/owner_setting/edit", views.edit_listing, name="edit_listing"),
    path("listing/<int:listing_id>/add_to_watchlist", views.edit_watchlist, name="add_watchlist"),
    path("listing/<int:listing_id>/leave_comment", views.leave_comment, name="leave_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/remove/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist")
]
