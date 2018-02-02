from django.db import models

from account import models as mod


class ClassRoutine(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    section = models.ForeignKey(mod.Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(mod.Subject, on_delete=models.CASCADE)

    day = models.CharField(max_length=30, null=True, blank=True)
    period = models.IntegerField(null=True, blank=True)
    start_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.day) + "-" + str(self.period)
