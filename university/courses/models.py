from django.db import models
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    credits = models.IntegerField(null=False, blank=False, default=4)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.course_name


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.course.course_name) + ' taken by ' + str(self.student.first_name)
