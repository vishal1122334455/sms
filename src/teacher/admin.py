from django.contrib import admin

from . import models

admin.site.register(models.Attendence)
admin.site.register(models.ClassTestExamTime)
admin.site.register(models.ClassTestExamMark)
