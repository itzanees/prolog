from django.contrib import admin

from .models import EquipmentHistory, Project


class EquipmentHistoryInline(admin.TabularInline):
    model = EquipmentHistory
    extra = 0
    fields = ("entry_date", "equipment", "activity", "quantity", "notes")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "project_no",
        "project_title",
        "client",
        "location",
        "start_date",
        "work_status",
        "updated_at",
    )
    list_filter = ("work_status", "start_date")
    search_fields = ("project_no", "client", "project_title", "location")
    date_hierarchy = "start_date"
    inlines = [EquipmentHistoryInline]


@admin.register(EquipmentHistory)
class EquipmentHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "entry_date",
        "equipment",
        "activity",
        "quantity",
    )
    list_filter = ("activity", "entry_date")
    search_fields = ("project__project_no", "project__project_title", "equipment")
