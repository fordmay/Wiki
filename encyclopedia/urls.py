from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
    path("create_new_page", views.create_new_page, name="create_new_page"),
    path("search", views.search, name="search"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("random_page", views.random_page, name="random_page")
]
