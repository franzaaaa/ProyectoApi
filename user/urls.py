from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views
from rest_framework.authtoken import views as v
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 


router = DefaultRouter()
router.register('user-list', views.UserApiView)


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/',views.CreateTokenView.as_view(), name='token'),
    path('me/',views.ManageUserView.as_view(), name='me'),
    path('me3/',v.obtain_auth_token,name='me3'),
    path('', include(router.urls)),
]