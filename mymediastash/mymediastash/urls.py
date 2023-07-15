from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
] \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if 'book' in settings.INSTALLED_APPS:
    urlpatterns += [path('book/', include('book.urls'))]


# handler404 = 'mymediastash.views.error_404'
# handler500 = 'mymediastash.views.error_500'
# handler403 = 'mymediastash.views.error_403'
# handler400 = 'mymediastash.views.error_400'
