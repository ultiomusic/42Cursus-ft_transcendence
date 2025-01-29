from django.urls import path, include
from . import views

from .views import index, GetUserViewSet, ReceivedFriendshipRequestViewSet, SentFriendshipRequestViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'user-list',GetUserViewSet, basename='user')
router.register(r'received-friendship-request', ReceivedFriendshipRequestViewSet, basename='rec-friendship-req')
router.register(r'sent-friendship-request', SentFriendshipRequestViewSet, basename='sent-friendship-req')


urlpatterns = [
    path("", index, name="home"),
    path('', include(router.urls)),
    path("login",views.login_page,name='login'),
    path("logout",views.logout_page,name='logout'),
    path("signup",views.signup_view,name='signup'),
    path('profile/', views.profile_view, name='profile'),
    

]