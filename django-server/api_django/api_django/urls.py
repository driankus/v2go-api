"""api_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# from volt_finder.apis import SignUpView, LogInView, LogOutView
from main.views import SignUpView, LogInView, LogOutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sign_up/', SignUpView.as_view(), name='sign_up'),
    path('api/log_in/', LogInView.as_view(), name='log_in'), 
    path('api/log_out/', LogOutView.as_view(), name='log_out'),
    path('api/volt_finder/', include('volt_finder.urls', 'cStation',)),
    path('api/', include('main.urls')), #TODO Do we need to add 'cStation' inside include() ?
]