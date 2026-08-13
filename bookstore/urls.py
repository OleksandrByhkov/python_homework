from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.http import JsonResponse


def health_check(request):
    return JsonResponse(
        {
            "status": "ok",
        }
    )


urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += i18n_patterns(
    path("", include("catalog.urls")),
    # path("orders/", include("orders.urls")),
)
