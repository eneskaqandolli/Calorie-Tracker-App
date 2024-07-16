from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="food_list"),
    path("<int:id>", views.delete, name="delete")
]
