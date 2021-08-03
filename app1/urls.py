from django.urls import path
from . import views

app_name = 'app1'

urlpatterns = [
    path('', views.WatchlistHomeIndex.as_view(), name='watchlist_index'),
    path('add_item/', views.WatchlistAddItem.as_view(), name='add_item'),
    path('edit_item/<int:pk>/', views.WatchlistUpdateItem.as_view(), name='edit_item'),
    path('price_history/<int:pk>', views.ProductPriceHistory, name='price_history'),
    path('add_scrape/', views.ScrapeAddInfo.as_view(), name='add_scrape')
]