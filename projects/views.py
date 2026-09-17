import csv

from rest_framework import viewsets, filters
from .serializers import ProjectSerializer

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import EquipmentHistoryForm, ProjectForm, EquipmentForm, EquipmentSupplier, EquipmentTypeForm, ProjectTaskForm, AddBoqForm
from .models import EquipmentHistory, Project, Equipment, EquipmentType, EquipmentSupplier, Task, BoqItem
from inventory.models import Inventory


def dashboard(request):
    all_projects = Project.objects.all()
    projects = all_projects
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    if query:
        projects = projects.filter(
            Q(project_no__icontains=query)
            | Q(client__icontains=query)
            | Q(project_title__icontains=query)
            | Q(location__icontains=query)
        )
    if status:
        projects = projects.filter(work_status=status)

    stats = {
        "total": all_projects.count(),
        "in_progress": all_projects.filter(
            work_status=Project.WorkStatus.IN_PROGRESS
        ).count(),
        "completed": all_projects.filter(
            work_status=Project.WorkStatus.COMPLETED
        ).count(),
        "on_hold": all_projects.filter(work_status=Project.WorkStatus.ON_HOLD).count(),
    }

    context = {
        "projects": projects,
        "query": query,
        "selected_status": status,
        "status_choices": Project.WorkStatus.choices,
        "project_type_choices": Project.ProjectTypes.choices,
        "stats": stats,
    }
    return render(request, "projects/dashboard.html", context)



def current_dashboard(request):
    return render(request, "projects/ongoing-projects-dashboard.html")

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['client', 'project_title', 'location', 'project_no']
    ordering_fields = '__all__'
    ordering = ['client']
    # Optionally add DjangoFilterBackend for status filtering
    # filterset_fields = ['is_completed', 'location', 'client']



def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.prefetch_related("equipment_history") & Project.objects.prefetch_related("project_tasks"), pk=pk
    )
    equipment_form = EquipmentHistoryForm(
        initial={"entry_date": timezone.localdate()}
    )

    project_task_form = ProjectTaskForm(
        initial = {"entry_date": timezone.localdate()}
    )

    return render(
        request,
        "projects/project_detail.html",
        {"project": project, "equipment_form": equipment_form, "project_task_form": project_task_form},
    )



def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, f"Project {project.project_no} was created successfully.")
            return redirect(project.get_absolute_url())
    else:
        form = ProjectForm()
    return render(
        request,
        "projects/project_form.html",
        {"form": form, "page_title": "Add project", "submit_label": "Create project"},
    )



def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, f"Project {project.project_no} was updated successfully.")
            return redirect(project.get_absolute_url())
    else:
        form = ProjectForm(instance=project)
    return render(
        request,
        "projects/project_form.html",
        {
            "form": form,
            "project": project,
            "page_title": "Edit project",
            "submit_label": "Save changes",
        },
    )


def equipments(request):
    all_equipments = Equipment.objects.all()
    equipments = all_equipments
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    if query:
        equipments = equipments.filter(
            Q(equipment_no__icontains=query)
            | Q(equipment_name__icontains=query)
            | Q(client__icontains=query)
            | Q(project_title__icontains=query)
            | Q(location__icontains=query)
        )
    if status:
        equipments = equipments.filter(equipment_status=status)

    stats = {
        "total": all_equipments.count(),
        "in_progress": all_equipments.filter(
            equipment_status=Equipment.EquipmentStatus.IN_PROGRESS
        ).count(),
        "completed": all_equipments.filter(
            equipment_status=Equipment.EquipmentStatus.COMPLETED
        ).count(),
        "on_hold": all_equipments.filter(equipment_status=Equipment.EquipmentStatus.ON_HOLD).count(),
    }

    context = {
        "equipments": equipments,
        "query": query,
        "selected_status": status,
        "status_choices": Project.WorkStatus.choices,
        "stats": stats,
    }
    print(equipments)

    return render(request, "equipments/dashboard.html", context)



def equipment_types(request):
    if request.method == "POST":
        form = EquipmentTypeForm(request.POST)
        if form.is_valid():
            equipment_type = form.save()
            messages.success(request, f"Equipment {equipment_type.equipment_type} was created successfully.")
            # return redirect('equipment_types')
    
    form = EquipmentTypeForm()
    equipment_types = EquipmentType.objects.all()
    print(equipment_types)
    return render(
        request,
        "equipments/equipment_type.html",
        {"form": form, "eqtypes" : equipment_types, "page_title": "Add equipment type", "submit_label": "Create type"},
    )



def equipment_create(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            messages.success(request, f"Equipment no: {equipment.equipment_no} - {equipment.equipment_manufacture} {equipment.equipment_type} was created successfully.")
    form = EquipmentForm()
    return render(
        request,
        "equipments/create_equipment.html",
        {"form": form, "page_title": "Add equipment", "submit_label": "Create Equipment"},
    )



@require_POST
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project_no = project.project_no
    project.delete()
    messages.success(request, f"Project {project_no} was deleted.")
    return redirect("projects:dashboard")




@require_POST
def task_add(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectTaskForm(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.project = project
        entry.save()
        messages.success(request, "New Task added.")
    else:
        messages.error(request, "Please correct the task form and try again.")
    return redirect(project.get_absolute_url())




def task_details(request, pk, task_pk):
    if request.method == "POST":
        return render(request)
    else:
        project = get_object_or_404(Project, pk=pk)
        task = get_object_or_404(Task, pk=task_pk)
        boq_form = AddBoqForm()
        return render(request, "projects/task_details.html", {"project":project, "task":task, "boq_form":boq_form})




def load_inventory_items(request):
    category_id = request.GET.get('boq_category')
    if category_id:
        items = Inventory.objects.filter(category_id=category_id).order_by('item')
    else:
        items = Inventory.objects.none()
    return render(request, 'projects/partials/inventory_options.html', {'items': items})




@require_POST
def task_delete(request, pk, entry_pk):
    project = get_object_or_404(Project, pk=pk)
    entry = get_object_or_404(Task, pk=entry_pk, project=project)
    entry.delete()
    messages.success(request, "Task entry removed.")
    return redirect(project.get_absolute_url())



@require_POST
def equipment_add(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = EquipmentHistoryForm(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.project = project
        entry.save()
        messages.success(request, "Equipment history entry added.")
    else:
        messages.error(request, "Please correct the equipment history form and try again.")
    return redirect(project.get_absolute_url())




@require_POST
def equipment_delete(request, pk, entry_pk):
    project = get_object_or_404(Project, pk=pk)
    entry = get_object_or_404(EquipmentHistory, pk=entry_pk, project=project)
    entry.delete()
    messages.success(request, "Equipment history entry removed.")
    return redirect(project.get_absolute_url())



def project_report(request, pk):
    project = get_object_or_404(
        Project.objects.prefetch_related("equipment_history"), pk=pk
    )
    return render(
        request,
        "projects/report.html",
        {"project": project, "equipment_entries": project.equipment_history.all()},
    )



def project_report_csv(request, pk):
    project = get_object_or_404(Project, pk=pk)
    entries = list(project.equipment_history.all())
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="project-{project.project_no}-report.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(
        [
            "PROJECT NO.",
            "CLIENT",
            "PROJECT TITLE",
            "LOCATION",
            "START DATE",
            "SCOPE OF WORK",
            "WORK STATUS",
            "REMAINING WORK",
            "EQUIPMENT HISTORY DATE",
            "EQUIPMENT",
            "ACTIVITY",
            "QUANTITY",
            "NOTES",
        ]
    )
    if entries:
        for entry in entries:
            writer.writerow(
                [
                    project.project_no,
                    project.client,
                    project.project_title,
                    project.location,
                    project.start_date,
                    project.scope_of_work,
                    project.get_work_status_display(),
                    project.remaining_work,
                    entry.entry_date,
                    entry.equipment_name,
                    entry.activity,
                    entry.quantity,
                    entry.notes,
                ]
            )
    else:
        writer.writerow(
            [
                project.project_no,
                project.client,
                project.project_title,
                project.location,
                project.start_date,
                project.scope_of_work,
                project.get_work_status_display(),
                project.remaining_work,
                "",
                "",
                "",
                "",
                "",
            ]
        )
    return response
