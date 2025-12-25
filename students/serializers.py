from rest_framework import serializers
from .models import Student, Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__' # Guruhning barcha ustunlarini JSON-ga o'giradi

class StudentSerializer(serializers.ModelSerializer):
    # Guruh haqida to'liq ma'lumot ko'rinishi uchun (ixtiyoriy)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'group', 'group_name', 'phone', 'added_at']