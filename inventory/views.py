
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Supplier, Uom, Category, Inventory
from .forms import  UomForm, CategoryForm, InventoryForm, SupplierForm

def inventory(request):
    inventory = Inventory.objects.all()
    low_stock = 0
    # for item in inventory
    stats = {
        "total": inventory.count(),
        "no_stock": inventory.filter(
            qty=0
        ).count(),
        'low_stock' : low_stock
        
    }
    return render(request,"inventory/dashboard.html",{'inventory':inventory, 'stats':stats})

def inventory_create(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save()
            messages.success(request, f"Project {inventory.item} was created successfully.")
            return redirect(inventory.get_absolute_url())
    else:
        form = InventoryForm()
    return render(
        request,
        "inventory/item_form.html",
        {"form": form, "page_title": "Add Inventory", "submit_label": "Create Item"},
    )

def uom(request):
    if request.method == "POST":
        form = UomForm(request.POST)
        if form.is_valid():
            uom = form.save()
            messages.success(request, f" {uom.uom} was created successfully.")
            return redirect(uom.get_absolute_url())
    else:
        form = UomForm()
        uoms = Uom.objects.all()
        return render(
            request,
            "inventory/uom.html",
            {"form": form, "page_title": "UoM", "uoms":uoms}
            )

def create_item(request):
    return render(request, "inventory/item_form.html")

def category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f" {cat.name} was created successfully.")
            return redirect('inventory:category')
    else:
        form = CategoryForm()
        categories = Category.objects.all()
        return render(request,"inventory/category.html", {'form':form, 'categories':categories})

def suppliers(request):
    suppliers = Supplier.objects.all()
    context = {
        'suppliers':suppliers,
       }
    return render(request,"inventory/suppliers.html", context)


def supplier_create(request):
    if request.method == "POST":
            form = SupplierForm(request.POST)
            if form.is_valid():
                supplier = form.save()
                messages.success(request, f" {supplier.name} was created successfully.")
                return redirect('inventory:suppliers')
    form = SupplierForm()
    return render(request, "inventory/supplier_form.html", {'form':form})

def supplier_details(request, pk):
    supplier = get_object_or_404(
        Supplier, pk=pk
    )

    return render(
        request,
        "inventory/supplier_details.html",
        {"supplier": supplier},
    )