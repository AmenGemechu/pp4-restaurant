from django.contrib import admin
from django.urls import path, include
# from exotic_cuisine.views import create_post


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('exotic_cuisine.urls', namespace='exotic_cuisine')),
    path('summernote/', include('django_summernote.urls')),
    path('', include('exotic_cuisine.urls'), name='exotic_cuisine_urls'),
    path('accounts/', include('allauth.urls')),
]

# handler403 = "helpers.views.handle_not_found"
