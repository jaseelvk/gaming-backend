from django.urls import path
from . import views

urlpatterns = [
    path("", views.products, name='products'),
    path("view/<int:pk>/", views.product, name='product'),
    path("tasks/create/", views.create_task, name='create_task'),
    path("wishlist/add/<int:pk>/", views.add_to_wishlist, name='add_to_wishlist'),
    path("wishlist/remove/<int:pk>/", views.remove_from_wishlist, name='remove_from_wishlist'),
    path("wishlist/", views.list_wishlist, name='list_wishlist'),
]
