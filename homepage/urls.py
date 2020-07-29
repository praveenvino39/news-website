from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('detail/<int:news_id>/<str:search_term>', views.detail, name='detail'),
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('saved/<int:news_id>/<str:search_term>', views.saved_news, name='saved_news'),
    path('saved_list', views.saved_list, name='saved_list'),
    path('saved_detail/<int:id>', views.saved_detail, name='saved_detail'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('search/', views.search, name='search'),
    path('search_detail/<int:news_id>/<str:search_term>', views.search_detail, name='search_detail'),
    path('saved_news_search/<int:news_id>/<str:search_term>', views.saved_news_search, name='save_news_search')


]