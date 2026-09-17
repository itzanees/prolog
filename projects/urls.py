from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from projects.views import ProjectViewSet


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

app_name = "projects"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dash", views.current_dashboard, name="currentdashboard"),
    path('api/', include(router.urls)),
    path("equipments/", views.equipments, name="equipments"),
    path("equipments/types", views.equipment_types, name="equipment_types"),
    path("equipments/new/", views.equipment_create, name="equipment_create"),
    # path("equipments/<int:pk>/", views.equipments_details, name="equipments_details"),
    # path("equipments/<int:pk>/edit", views.equipments_update, name="equipments_update"),
    # path("equipments/<int:pk>/delete", views.equipments_delete, name="equipments_delete"),
    path("projects/new/", views.project_create, name="project_create"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("projects/<int:pk>/edit/", views.project_update, name="project_update"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),
    path("projects/<int:pk>/equipment/add/", views.equipment_add, name="equipment_add"),
    path("projects/<int:pk>/task/add/", views.task_add, name="task_add"),
    path("projects/<int:pk>/task/<int:entry_pk>/delete/", views.task_delete, name="task_delete"),
    path("projects/<int:pk>/task/<int:task_pk>", views.task_details, name="task_details"),
    path('ajax/load-inventory-items/', views.load_inventory_items, name='ajax_load_inventory_items'),
    path(
        "projects/<int:pk>/equipment/<int:entry_pk>/delete/",
        views.equipment_delete,
        name="equipment_delete",
    ),
    path("projects/<int:pk>/report/", views.project_report, name="project_report"),
    path(
        "projects/<int:pk>/report.csv",
        views.project_report_csv,
        name="project_report_csv",
    ),
]
