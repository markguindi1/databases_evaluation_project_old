from django.db import models
from django.utils import timezone

# Create your models here.


class Student(models.Model):
    stud_id = models.CharField(max_length=15, primary_key=True)
    stud_pswd = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.stud_id + ")"



class Professor(models.Model):
    prof_id = models.CharField(max_length=15, primary_key=True)
    prof_pswd = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.prof_id + ")"


class Course(models.Model):
    course_num = models.CharField(max_length=20)
    prof_id = models.ForeignKey(Professor, null=True, on_delete=models.SET_NULL)
    # Use of ManyToManyField is for Django conventions.
    # Otherwise, the Enrollment table would be used.
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.course_num

'''
class Enrollment(models.Model):
    stud_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
'''

class Session(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    session_start = models.DateTimeField()
    session_end = models.DateTimeField()

    def __str__(self):
        return str(self.pk)

    def is_open(self):
        return self.session_start < timezone.now() < self.session_end

class Comment(models.Model):
    stud_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    class_rating = models.CharField(max_length=15, blank=True)
    class_comment = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return str(self.pk)

    def can_edit(self):
        return self.session_id.session_start < timezone.now() < self.session_id.session_end
