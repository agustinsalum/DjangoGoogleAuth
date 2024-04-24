from django.contrib import admin

from noteApp.models import UserProfile, Note

# Register your models here.

@admin.register(UserProfile)
class LessonAdmin(admin.ModelAdmin):
    pass

@admin.register(Note)
class LessonAdmin(admin.ModelAdmin):
    pass
