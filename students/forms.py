from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}

    def clean_section(self):
        return self.cleaned_data["section"].strip().upper()


# How the Add / Edit page groups the fields
SECTIONS = [
    ("Academic information", ["student_number", "program", "year_level", "section",
                              "academic_year", "status"]),
    ("Personal & contact information", ["first_name", "last_name", "preferred_name", "email",
                                        "date_of_birth", "mobile", "city_province", "home_address"]),
    ("Family background", ["father_name", "mother_name", "guardian_name",
                           "guardian_relationship", "guardian_contact"]),
]