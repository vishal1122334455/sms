from django.db import models

from account import models as mod


class Attendence(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    section = models.ForeignKey(mod.Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(mod.Subject, on_delete=models.CASCADE)
    teachers = models.ForeignKey(mod.UserProfile, on_delete=None, related_name='teachers')

    date = models.DateField(auto_now_add=True)
    students = models.ManyToManyField(mod.UserProfile, related_name='students')


    def __str__(self):
        return str(self.school.name) + "-" + str(self.classes.name) + ":" + str(self.subject.name) + ":" + str(self.date)


    @classmethod
    def addStudent(cls, request, newStudent, id):
        student, created = cls.objects.get_or_create(
            id=id,
        )

        student.students.add(newStudent)

    @classmethod
    def removeStudent(cls, request, newStudent, id):
        student, created = cls.objects.get_or_create(
            id=id,
        )

        student.students.remove(newStudent)



#class test exam time
class ClassTestExamTime(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    section = models.ForeignKey(mod.Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(mod.Subject, on_delete=models.CASCADE)
    teachers = models.ForeignKey(mod.UserProfile, on_delete=None)

    exam_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.classes.name) + "-" + str(self.section.name) + "-" + str(self.id)



#class test exam marks
class ClassTestExamMark(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    section = models.ForeignKey(mod.Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(mod.Subject, on_delete=models.CASCADE)
    teachers = models.ForeignKey(mod.UserProfile, on_delete=None, related_name='adder')

    student = models.ForeignKey(mod.UserProfile, on_delete=None, related_name='added', null=True, blank=True)
    exam = models.ForeignKey(ClassTestExamTime, on_delete=models.CASCADE)
    mark = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.classes.name) + "-" + str(self.section.name) + "-" + str(self.exam.id)



#office notice model
class Notice(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE, related_name='teacher_school')
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE, related_name='student_class')
    user = models.ForeignKey(mod.UserProfile, on_delete=models.CASCADE, related_name='teacher_notice')

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.classes.name) + "-" + str(self.user.username)
