from django.urls import path
from .views import item_detail, item_index, item_cart, item_purchase
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, CartViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'carts', CartViewSet)

app_name = 'item'

urlpatterns = [
    path('index/', item_index, name='index'),
    path('<int:id>/', item_detail, name='detail'),
    path('cart/', item_cart, name='cart'),
    path('purchase/', item_purchase, name='purchase'),
    path('', include(router.urls)),
    
]
