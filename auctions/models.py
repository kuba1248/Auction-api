from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from django.utils import timezone


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

    def is_watchers(self, listing):
        return listing in self.watchlists.all()

    def number_of_created_listings(self):
        return self.created_listings.all().count()

    def get_joined_date(self):
        return self.date_joined.strftime("%m/%d/%Y")


class Category(models.Model):
    category = models.CharField(max_length=64)

    class Meta:
        ordering = ('category',)

    def __str__(self):
        return self.category


class Listing(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1000)
    image = models.URLField(
        max_length = 1000,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="listings"
    )
    active = models.BooleanField(default=True)
    condition_choices = [("","---------"), ("New", "Brand New"), ("Used once", "Used once"), ("Used", "Used")]
    condition = models.CharField(max_length=9, choices=condition_choices, default='""')
    start_datetime = models.DateTimeField(default=timezone.now())
    end_datetime = models.DateTimeField(default=timezone.now)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
    current_bid = models.DecimalField(
        blank=True,
        null=True,
        max_digits=7,
        decimal_places=2
    )
    owner = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.PROTECT, related_name="created_listings"
    )
    winner = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="win_items"
    )
    watchers = models.ManyToManyField(
        User, blank=True, related_name="watchlists")

    class Meta:
        ordering = ('start_datetime',)

    def __str__(self):
        return f"{self.id}: {self.title}"

    def number_of_bids(self):
        return self.bids.all().count()
    
    def get_current_bid(self):
        if self.number_of_bids() > 0:
            highest_bid = self.bids.aggregate(Max("amount"))
            self.current_bid = round(highest_bid["amount__max"],2)
            return self.current_bid

        self.current_bid = self.starting_bid
        return self.current_bid
    
    def get_winner(self):
        if (self.number_of_bids() > 0):
            winner = self.bids.get(amount = self.get_current_bid()).user
            if winner is not None:
                self.winner = winner
            return self.winner
        return None

    def deactivate(self):
        self.get_winner()
        self.end_datetime = timezone.now()
        self.active = False
    
    def activate(self):
        self.winner = None
        self.end_datetime = None
        self.active = True


class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    datetime = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ("amount",)
    
    def __str__(self):
        return f"Bid#{self.id}: {self.amount} on {self.auction.title} by {self.user.username}"


class Comment(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    datetime = models.DateTimeField(default=timezone.now())
    content = models.TextField(max_length=256)

    class Meta:
        ordering = ("datetime",)
    
    def __str__(self):
        return f"Comment#{self.id}: {self.content} on {self.auction.title} by {self.user.username}"