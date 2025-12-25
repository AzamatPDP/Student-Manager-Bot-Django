from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Guruh nomi")
    direction = models.CharField(max_length=100, verbose_name="Yo'nalishi")

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ismi")
    last_name = models.CharField(max_length=100, verbose_name="Familiyasi")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="students")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"