"""
URL configuration for box_selector project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
from shipping import views as shipping_views
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from shipping import views as shipping_views
# We are from django.urls import include for including the URLs from the shipping app. The include() function allows us to reference other URLconfs. In this case, we are including the URLs defined in the shipping app's urls.py file.

urlpatterns = [
    # By default, Django includes the admin site at the URL path /admin/. You can customize this path by changing the argument to the path() function. For example, if you want to change the admin site URL to /myadmin/, you can modify the urlpatterns list as follows here:
    path('admin/', admin.site.urls),
    
    # The line path("api/", include("shipping.urls")) includes the URL patterns defined in the shipping app's urls.py file under the /api/ path. This means that any URL starting with /api/ will be handled by the views defined in the shipping app. For example, the URL /api/recommend-box/ will be routed to the recommend_box_view function in shipping/views.py, and /api/orders/<reference>/box/ will be routed to the order_box_view function in shipping/views.py.
    path("api/", include("shipping.urls")),
    path("favicon.ico", shipping_views.favicon_view),
    path("", shipping_views.home_view, name="home"),
]

