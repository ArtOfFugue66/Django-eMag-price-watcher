from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import query
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from app1.models import WatchItem, Scrape
from . import forms


class WatchlistHomeIndex(LoginRequiredMixin, ListView):
    """
    Listing of all current items in the user's watchlist
    """
    model = WatchItem
    template_name = 'app1/watchlist_index.html'

    """
    Only show watchlist items added by the logged in user
    """
    def get_queryset(self):
        queryset = super(WatchlistHomeIndex, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


@login_required(login_url="/")
def add_item_view(request):
    """
    Adding an item to the watchlist
    """
    if request.method == 'POST':
        form = forms.AddItemForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('app1:watchlist_index')
    else:
        form = forms.AddItemForm()
    return render(request, 'app1/watchlist_add_item.html', {'form': form})


# class WatchlistDeleteItem(LoginRequiredMixin, DeleteView):
#     model = WatchItem
#     template_name = 'app1/watchlist_index.html'
#     success_url = reverse_lazy('watchlist_index')

def watchlist_delete_item(request, pk):
    item = WatchItem.objects.get(id=pk)
    item.delete()
    return redirect("app1:watchlist_index")



class WatchlistUpdateItem(LoginRequiredMixin, UpdateView):
    model = WatchItem
    fields = ['name', 'url']
    template_name = 'app1/watchlist_edit_item.html'

    def get_success_url(self):
        return reverse('app1:watchlist_index')

import plotly.offline as opy
import plotly.graph_objs as go
from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.cache import cache

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
                
        cache.clear()

        x_data = dateTimes
        y_data = prices
        plot_div = opy.plot([go.Scatter(x=x_data, y=y_data, mode="markers+lines", name='Price history', opacity=0.8, marker_color='blue')], output_type='div')

        return render(request, "graph.html", context={'plot_div': plot_div})
