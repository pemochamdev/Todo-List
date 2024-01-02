from django.contrib import admin

# Register your models here.
from todoapp.models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'status']

