from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.templatetags.static import static as tag_static
from django.urls import include, path
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(
    url=tag_static('general/img/logo.png'),
    permanent=True,
)


def index_view(request):
    return (
        redirect('dashboard')
        if request.user.is_authenticated
        else redirect('sign_in')
    )


urlpatterns = [
    path('', index_view),
    path('favicon.ico', favicon_view),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('edifices.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        *debug_toolbar_urls(),
        path('__reload__/', include('django_browser_reload.urls')),
    ]
