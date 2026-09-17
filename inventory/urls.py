from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.inventory, name="inventory"),
    path("create", views.inventory_create, name="inventory_create"),
    path("uom", views.uom, name="uom"),
    # path("uom", views.create_item, name="create_item"),
    path("category", views.category, name="category"),
    path("suppliers", views.suppliers, name="suppliers"),
    path("suppliers/create", views.supplier_create, name="supplier_create"),
    path("suppliers/<int:pk>", views.supplier_details, name="supplier_details"),

]
