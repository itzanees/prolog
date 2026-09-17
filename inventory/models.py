from django.db import models
from django.urls import reverse

class Supplier(models.Model):
    name = models.CharField(max_length=250, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    email = models.EmailField(blank=True, null=True)
    cr_no = models.CharField(max_length=30,blank=True,null=True)
    vat_id = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True,null=True)
    bank_account_no = models.PositiveIntegerField(blank=True, null=True)
    bank_iban_no = models.CharField(max_length=24,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("inventory:supplier_details", args=[self.pk])

class Category(models.Model):
    name = models.CharField(max_length=50)
    category_code = models.CharField(max_length=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Uom(models.Model):
    uom = models.CharField("Unit of Measure", max_length=25)
    symbol = models.CharField("UoM short form", max_length=10,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Unit of Measure"
        verbose_name_plural = "Units of Measure"
        ordering = ["uom"]

    def __str__(self):
        return self.uom
    
    def get_absolute_url(self):
        return reverse("inventory:uom")
    
class Inventory(models.Model):
    class StockStatus(models.TextChoices):
            NO_STOCK = "No Stock", "No Stock"
            LOW_STOCK = "Low Stock", "Low Stock"
            
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="inventory_items"
    )
    item = models.CharField(max_length=200, unique=True)
    length = models.CharField("Length in mm",max_length=50, blank=True, null=True)
    width = models.CharField("Height in mm",max_length=50, blank=True, null=True)
    uom = models.ForeignKey(
        Uom, on_delete=models.PROTECT, related_name="inventory_items"
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.PositiveIntegerField("Quantity", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"
        ordering = ["item"]

    def __str__(self):
        return f"{self.item} ({self.qty} {self.uom})"



