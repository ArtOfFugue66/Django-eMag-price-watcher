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

import plotly.offline as opy
import plotly.graph_objs as go
from django.views.generic import TemplateView
from django.shortcuts import render

# def GraphView(request, userID):
class GraphView(LoginRequiredMixin, TemplateView):
    def get(self, request, pk):
        # Fetch scraped prices for the selected product
        scrapes = Scrape.objects.filter(item=pk)
        pricesQS, dateTimesQS = scrapes.values('price'), scrapes.values('dateTime')
        
        prices, dateTimes = [], []
        for priceDict in pricesQS:
            prices.append(priceDict['price'])
        for dateTimeDict in dateTimesQS:
            dateTimes.append(dateTimeDict['dateTime'])
                
        x_data = dateTimes
        y_data = prices
        # plot_div = opy.plot([go.Scatter(x=x_data, y=y_data, mode="lines", name='Price history', opacity=0.8, marker_color='red')], output_type='div')
        plot_div2 = opy.plot([go.Scatter(x=x_data, y=y_data, mode="lines", name='Price history', opacity=0.8, marker_color='blue')], output_type='div')

        return render(request, "graph.html", context={'plot_div': plot_div2})
