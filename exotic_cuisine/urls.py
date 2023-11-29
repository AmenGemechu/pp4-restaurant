from . import views
# from django. http import HttpResponse
from django.urls import path
from .views import ArticleDetailView, AddPostView, UpdatePostView  # IndexView


app_name = 'exotic_cuisine'

# are read top to bottom
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('article/edit/<int:pk>/', UpdatePostView.as_view(), name='update_post'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    # path('register/', views.registerPage, name='register'),
    path('login_user/', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),



    # path('', views.IndexView.as_view(), name='index'),

    # path('posts/', views.PostsView.as_view(), name='posts'),
    # path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
]
