from django.urls import path 
from .import views
from django.views.generic import TemplateView

# url configration
urlpatterns = [
    # path('playground/hello', views.say_hello) we don't need since we add our urls file in store front 
    path('hello/', views.say_hello),
    # path('greetings/', views.greetings) # function based view
    # path('greetings/', views.HelloView.as_view()) # class based view
    path('', TemplateView.as_view(template_name='core/index.html')) # class based view
]