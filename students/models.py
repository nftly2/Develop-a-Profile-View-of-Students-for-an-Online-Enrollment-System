from django.db import models


class Student(models.Model):
    PROGRAMS = [
        ("BSIT", "BS Information Technology (BSIT)"),
        ("BSCS", "BS Computer Science (BSCS)"),
        ("BSPA", "BS Public Administration (BSPA)"),
        ("BSBA", "BS Business Administration (BSBA)"),
        ("BSED", "BS Education (BSED)"),
    ]
    YEARS = [(1, "1st year"), (2, "2nd year"), (3, "3rd year"), (4, "4th year")]
    STATUS = [("Enrolled", "Enrolled"), ("Pending", "Pending"), ("Dropped", "Dropped")]

    # Academic information
    student_number = models.CharField(max_length=20, unique=True)
    program = models.CharField(max_length=10, choices=PROGRAMS)
    year_level = models.PositiveSmallIntegerField(choices=YEARS)
    section = models.CharField(max_length=5, help_text="Example: A")
    academic_year = models.CharField(max_length=20, default="2026-2027")
    status = models.CharField(max_length=20, choices=STATUS, default="Enrolled")

    # Personal & contact information
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    preferred_name = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    city_province = models.CharField("City / province", max_length=100, blank=True)
    home_address = models.CharField(max_length=200, blank=True)

    # Family background
    father_name = models.CharField(max_length=120, blank=True)
    mother_name = models.CharField(max_length=120, blank=True)
    guardian_name = models.CharField(max_length=120, blank=True)
    guardian_relationship = models.CharField(max_length=60, blank=True)
    guardian_contact = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self):
        return (self.first_name[:1] + self.last_name[:1]).upper()

    @property
    def year_section(self):
        return f"{self.year_level}-{self.section}"

    @property
    def color_index(self):
        return self.pk % 4 if self.pk else 0