from django.urls import path
from .views import (
    HomeView, ContactsView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    ProductPublishView
)

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/publish/', ProductPublishView.as_view(), name='product_publish'),
]