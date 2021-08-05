from django.urls import path
from . import views

app_name = 'app1'

urlpatterns = [
    path('', views.WatchlistHomeIndex.as_view(), name='watchlist_index'),
    path('add_item/', views.add_item_view, name='add_item'),
    path('edit_item/<int:pk>/', views.WatchlistUpdateItem.as_view(), name='edit_item'),
    path('delete_item/<int:pk>/', views.watchlist_delete_item, name="delete_item"),
    path('price_history/<int:pk>', views.GraphView.as_view(), name='price_history')
]