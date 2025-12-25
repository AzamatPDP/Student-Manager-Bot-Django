from django.contrib import admin
from .models import Student, Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'student_count')
    search_fields = ('name', 'direction')

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "Talabalar soni"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'group', 'phone', 'added_at') # Jadval ustunlari
    list_filter = ('group', 'added_at') # O'ng tomonda filtrlash
    search_fields = ('first_name', 'last_name', 'phone') # Qidiruv oynasi
    date_hierarchy = 'added_at' # Vaqt bo'yicha navigatsiya