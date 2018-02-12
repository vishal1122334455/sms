from django.conf.urls import url

from . import views



urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),

    #attendance module start

    url(r'^attendance/class-list/$', views.AttendanceClassList.as_view(), name='attendance-class-list'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/section-list/$', views.AttendanceSectionList.as_view(), name='attendance-section-list'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/subject-list/$', views.AttendanceSubjectList.as_view(), name='attendance-subject-list'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/(?P<subject_id>[0-9]+)/all/$', views.AttendanceSubjectAll.as_view(), name='attendance-subject-all'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/(?P<attendance_id>[0-9]+)/create/$', views.AttendanceCreate.as_view(), name='attendance-create'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/(?P<subject_id>[0-9]+)/statistics/$', views.AttendanceSubjectWiseStatistics.as_view(), name='attendance-subject-wise-statistics'),

    #end attendance module


    #start exam and marks module


    url(r'^exam-and-marks/$', views.ExamAndMarksHome.as_view(), name='exam-and-marks-home'),
    url(r'^exam-and-marks/class-list/$', views.ExamAndMarksClassList.as_view(), name='exam-and-marks-class-list'),
    url(r'^exam-and-marks/(?P<classes>[a-zA-Z0-9-_]+)/section-list/$', views.ExamAndMarksSectionList.as_view(), name='exam-and-marks-section-list'),
    url(r'^exam-and-marks/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/subject-list/$', views.ExamAndMarksSubjectList.as_view(), name='exam-and-marks-subject-list'),
    url(r'^exam-and-marks/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/(?P<subject_id>[0-9]+)/all/$', views.ExamAndMarksSubjectAllExam.as_view(), name='exam-and-marks-subject-all-exam'),
    url(r'^exam-and-marks/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/(?P<subject_id>[0-9]+)/create/$', views.ExamAndMarksExamCreate.as_view(), name='exam-and-marks-exam-create'),
    url(r'^exam-and-marks/(?P<pk>[0-9]+)/edit/$', views.ExamAndMarksExamEdit.as_view(), name='exam-and-marks-exam-edit'),
    url(r'^exam-and-marks/(?P<pk>[0-9]+)/delete/$', views.ExamAndMarksExamDelete.as_view(), name='exam-and-marks-exam-delete'),


    url(r'^exam-and-marks/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/(?P<subject_id>[0-9]+)/(?P<exam_id>[0-9]+)/student/$', views.ExamAndMarksExamStudent.as_view(), name='exam-and-marks-exam-student'),
    url(r'^exam-and-marks/(?P<exam_id>[0-9]+)/marks/$', views.ExamAndMarksView.as_view(), name='exam-and-marks-view'),

    url(r'^exam-and-marks/mark/(?P<pk>[0-9]+)/edit/$', views.ExamAndMarksEdit.as_view(), name='exam-and-marks-edit'),
    url(r'^exam-and-marks/mark/(?P<pk>[0-9]+)/delete/$', views.ExamAndMarksDelete.as_view(), name='exam-and-marks-delete'),


    #end exam and marks module


    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::api::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    url(r'^attendance/api/$', views.AttendanceAPIPresent.as_view(), name='attendence-api'),

]
