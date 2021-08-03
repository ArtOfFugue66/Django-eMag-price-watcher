from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import query
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from app1.models import WatchItem, Scrape


class WatchlistHomeIndex(LoginRequiredMixin, ListView):
    """
    Listing of all current items in the user's watchlist
    """
    model = WatchItem
    template_name = 'app1/watchlist_index.html'

    def get_queryset(self):
        queryset = super(WatchlistHomeIndex, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class WatchlistAddItem(LoginRequiredMixin, CreateView):
    """
    Adding an item to the watchlist
    """
    model = WatchItem
    fields = '__all__'
    template_name = 'app1/watchlist_add_item.html'

    # Path to redirect to when the form is successfully validated
    def get_success_url(self):
        return reverse("app1:watchlist_index")


class WatchlistUpdateItem(LoginRequiredMixin, UpdateView):
    model = WatchItem
    fields = '__all__'
    template_name = 'app1/watchlist_add_item.html'

    def get_success_url(self):
        return reverse('app1:watchlist_index')


class ProductPriceHistory(LoginRequiredMixin):
    ### TODO: try putting scraping code here & making a view similar to
    ###       what the guy in the codeburs.io tutorial is doing
    pass


class ScrapeAddInfo(CreateView):
    model = Scrape
    fields = '__all__'
    template_name = 'app1/scrape_page.html'

    # def get_success_url(self):
    #     return reverse('app1:watchlist_index')

