from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SECTIONS, StudentForm
from .models import Student


def student_list(request):
    q = request.GET.get("q", "").strip()
    year = request.GET.get("year", "")
    section = request.GET.get("section", "")

    students = Student.objects.all()
    if q:
        students = students.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(student_number__icontains=q)
        )
    if year.isdigit():
        students = students.filter(year_level=year)
    if section:
        students = students.filter(section=section)

    # Which student is open on the right side
    selected = None
    sid = request.GET.get("s", "")
    if sid.isdigit():
        selected = Student.objects.filter(pk=sid).first()
    if selected is None:
        selected = students.first()

    context = {
        "students": students,
        "selected": selected,
        "q": q,
        "year": year,
        "section": section,
        "years": Student.YEARS,
        "sections": Student.objects.order_by("section").values_list("section", flat=True).distinct(),
    }
    return render(request, "students/student_list.html", context)


def _form_page(request, form, title):
    sections = [(heading, [form[n] for n in names]) for heading, names in SECTIONS]
    return render(request, "students/student_form.html",
                  {"form": form, "sections": sections, "title": title})


def add_student(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        student = form.save()
        return redirect(f"/?s={student.pk}")
    return _form_page(request, form, "Add student")


def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f"/?s={student.pk}")
    return _form_page(request, form, f"Edit {student.full_name}")


@require_POST
def delete_student(request, pk):
    get_object_or_404(Student, pk=pk).delete()
    return redirect("student_list")