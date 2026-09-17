from django.db import models
from django.urls import reverse
from django.conf import settings

from inventory.models import Category, Uom, Inventory

class Project(models.Model):
    class WorkStatus(models.TextChoices):
        PLANNING = "Planning", "Planning"
        IN_PROGRESS = "In Progress", "In Progress"
        ON_HOLD = "On Hold", "On Hold"
        COMPLETED = "Completed", "Completed"
        CANCELLED = "Cancelled", "Cancelled"

    class ProjectTypes(models.TextChoices):
        INSTALLATION = "Instalaltion Only", "Installation Only"
        SUPPLY = "Supply Only", "Supply Only"
        SUPPLY_INSTALLATION = "Supply and Installation", "Supply and Installation"

    project_no = models.CharField(
        "PROJECT NO.", max_length=50, unique=True, db_column="PROJECT NO."
    )
    client = models.CharField("CLIENT", max_length=200, blank=True, db_column="CLIENT")
    project_title = models.CharField(
        "PROJECT TITLE", max_length=255, blank=True, db_column="PROJECT TITLE"
    )
    location = models.CharField("LOCATION", max_length=255, blank=True, db_column="LOCATION")
    start_date = models.DateField(
        "START DATE", null=True, blank=True, db_column="START DATE"
    )
    scope_of_work = models.TextField(
        "SCOPE OF WORK", blank=True, db_column="SCOPE OF WORK"
    )
    project_type = models.CharField(
        "PROJECT TYPE",
        max_length=30,
        choices=ProjectTypes.choices,
        default=ProjectTypes.INSTALLATION,
        db_column="PROJECT TYPE",
    )

    work_status = models.CharField(
        "WORK STATUS",
        max_length=30,
        choices=WorkStatus.choices,
        default=WorkStatus.PLANNING,
        db_column="WORK STATUS",
    )
    work_status_detail = models.TextField(
        "WORK STATUS DETAIL", blank=True, help_text="Original progress note from the source workbook."
    )
    remaining_work = models.TextField(
        "REMAINING WORK", blank=True, db_column="REMAINING WORK"
    )

    # manager = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, 
    #     on_delete=models.CASCADE, 
    #     related_name='managed_projects'
    # )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date", "project_no"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        indexes = [
            models.Index(fields=["work_status"]),
            models.Index(fields=["client"]),
            models.Index(fields=["start_date"]),
        ]

    def __str__(self):
        return f"{self.project_no} — {self.project_title}"

    def get_absolute_url(self):
        return reverse("projects:project_detail", args=[self.pk])

    @property
    def equipment_count(self):
        return self.equipment_history.count()
    
    @property
    def tasks_count(self):
        return self.project_tasks.count()

class Task(models.Model):
    STATUSES = [
        ('open', 'Open'),
        ('working','Working'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
        ('pending review','Pending Review')
    ]
    PRIORITIES = [
        ('low','Low'),
        ('medium','Medium'),
        ('high','High'),
        ('urgent','Urgent')
    ]
    project = models.ForeignKey(
            Project,
            on_delete=models.CASCADE,
            related_name="project_tasks",
            verbose_name="PROJECT",
            null=True,
            blank=True
        )
    subject = models.CharField(max_length=250, unique=True)
    status = models.CharField(max_length=25, choices=STATUSES)
    priority = models.CharField(max_length=25,choices=PRIORITIES)
    entry_date = models.DateField("DATE", null=True, blank=True)



class EquipmentType(models.Model):
    equipment_type = models.CharField("EQIPMNENT TYPE", max_length=25, unique=True)
    equipment_properties = models.TextField("PROPERTIES", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-equipment_type"]
        verbose_name = "Equipment types entry"
        verbose_name_plural = "Equipment types"
        indexes = [
            models.Index(fields=["equipment_type"]),
        ]

    def __str__(self):
        return f"{self.equipment_type}"

    def get_absolute_url(self):
            return reverse("projects:project_detail", args=[self.pk])

class EquipmentSupplier(models.Model):
    supplier_name = models.CharField("SUPPLIER", max_length=50)
    supplier_address = models.TextField("Address")
    supplier_phone = models.CharField("CONTACT NO", max_length=10)
    supplier_email = models.EmailField("SUPPLIER_EMAIL")
    contact_person = models.CharField("CONTACT PERSON", max_length=50)
    contact_person_phone = models.CharField("CONTACT PERSON PHONE", max_length=50)
    contact_person_email = models.EmailField("CONTACT PERSON EMAIL")
    equipment_rent = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Equipment(models.Model):
    class EquipmentStatus(models.TextChoices):
        BOOKED = "Booked", "Booked"
        IN_PROGRESS = "In Progress", "In Progress"
        ON_HOLD = "On Hold", "On Hold"
        COMPLETED = "Completed", "Completed"
        CANCELLED = "Cancelled", "Cancelled"
        RETURNED = "Returned", "Returned"

    equipment_no = models.CharField("EQPT NO", max_length=5, null=True, unique=True)
    equipment_slno = models.CharField("SLNO", max_length=15,  null=True, unique=True)
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name="type_of_equipment",
        verbose_name="EQUIPMENT TYPE",
        null=True
    )
    equipment_supplier = models.ForeignKey(
        EquipmentSupplier,
        on_delete=models.PROTECT,
        blank=True,
        null=True
        )
    equipment_manufacture = models.CharField(max_length=30, null=True)
    equipment_status = models.CharField(
                "WORK STATUS",
                max_length=30,
                choices=EquipmentStatus.choices,
                default=EquipmentStatus.BOOKED,
                db_column="EQUIPMENT STATUS",
            )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            ordering = ["-equipment_no"]
            verbose_name = "Equipment entry"
            verbose_name_plural = "Equipments"
            indexes = [
                models.Index(fields=["equipment_type"]),
            ]
    
    def __str__(self):
        return f"{self.equipment_no}. {self.equipment_type}-({self.equipment_slno})"


class EquipmentHistory(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="equipment_history",
        verbose_name="PROJECT",
    )
    entry_date = models.DateField("DATE", null=True, blank=True)
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE
    )
    start_date = models.DateField("STARTDATE", null=True, blank=True)

    activity = models.CharField(
        "ACTIVITY", max_length=100, help_text="For example: Issued, Returned, Serviced"
    )
    quantity = models.PositiveIntegerField("QUANTITY", default=1)
    notes = models.TextField("NOTES", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-entry_date", "-created_at"]
        verbose_name = "Equipment history entry"
        verbose_name_plural = "Equipment history"
        indexes = [
            models.Index(fields=["project", "entry_date"]),
            models.Index(fields=["equipment"]),
        ]

    def __str__(self):
        return f"{self.equipment} — {self.activity} ({self.entry_date:%d %b %Y})"


class BoqItem(models.Model):
    boq_category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="boq_items"
    )
    boq_item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    boq_size = models.CharField(max_length=50, blank=True, null=True)
    boq_uom = models.ForeignKey(
        Uom, on_delete=models.PROTECT, related_name="boq_items"
    )
    boq_qty = models.PositiveIntegerField("BOQ Quantity", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "BOQ Item"
        verbose_name_plural = "BOQ Items"
        ordering = ["boq_item"]

    def __str__(self):
        return f"{self.boq_item} ({self.boq_qty} {self.boq_uom})"