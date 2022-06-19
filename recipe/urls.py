from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views


router = DefaultRouter()
router.register('ingredient', views.IngredientViewSet)
router.register('product-list', views.ProductViewSet)
router.register('carrito-list',views.CarritoViewSet)
router.register('mods-list',views.ModsViewSet)
app_name = 'recipe'

urlpatterns = [
    # path('tag-list/', views.TagApiView.as_view(), name='tag-list'),
    path('', include(router.urls)),
]