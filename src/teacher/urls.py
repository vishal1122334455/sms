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


    #:::::start notice module url:::::
    #:::::::::::::::::::::::::::::::::

    url(r'^notice/$', views.Notice.as_view(), name='notice'),
    url(r'^notice/create/$', views.NoticeCreate.as_view(), name='notice-create'),
    url(r'^notice/class-list/$', views.NoticeClassList.as_view(), name='notice-class-list'),
    url(r'^notice/class-list/(?P<classes>[a-zA-Z0-9]+)/$', views.NoticeList.as_view(), name='notice-list'),
    url(r'^notice/view/(?P<pk>[0-9]+)/$', views.NoticeView.as_view(), name='notice-view'),
    url(r'^notice/edit/(?P<pk>[0-9]+)/$', views.NoticeEdit.as_view(), name='notice-edit'),
    url(r'^notice/delete/(?P<pk>[0-9]+)/$', views.NoticeDelete.as_view(), name='notice-delete'),
    url(r'^notice/search/$', views.NoticeSearch.as_view(), name='notice-search'),

    #::::::end notice module url::::::
    #:::::::::::::::::::::::::::::::::


    #::::start schedule module url::::
    #:::::::::::::::::::::::::::::::::


    url(r'^schedule/$', views.Schedule.as_view(), name='schedule'),
    url(r'^schedule/class-list/$', views.ClassList.as_view(), name='class-list'),
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/$', views.SectionList.as_view(), name='section-list'),

    #create routine
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/(?P<section>[a-zA-Z0-9-_]+)/routine/view/$', views.RoutineView.as_view(), name='routine-view'),

    #create exam routine
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/exam-routine/view/$', views.ExamRoutineView.as_view(), name='exam-routine-view'),


    #::::end schedule module url::::
    #:::::::::::::::::::::::::::::::::


    #:::::start teacher module url::::
    #:::::::::::::::::::::::::::::::::



    url(r'^teacher-detail/$', views.TeacherDetail.as_view(), name='teacher-detail'),


    #::::end schedule module url::::
    #:::::::::::::::::::::::::::::::



    #::::start schedule module url::::
    #:::::::::::::::::::::::::::::::::



    url(r'^student/$', views.StudentHome.as_view(), name='student-home'),
    url(r'^student/class-list/$', views.StudentClassList.as_view(), name='student-class-list'),
    url(r'^student/class-list/(?P<classes>[a-zA-Z0-9]+)/$', views.StudentSectionList.as_view(), name='student-section-list'),
    url(r'^student/class-list/(?P<classes>[a-zA-Z0-9]+)/(?P<section>[a-zA-Z0-9-_]+)/$', views.StudentList.as_view(), name='student-list'),

    url(r'^student/search/$', views.StudentSearch.as_view(), name='student-search'),
    url(r'^student/detail/(?P<pk>[0-9]+)/$', views.StudentDetail.as_view(), name='student-detail'),


    #::::end schedule module url::::
    #:::::::::::::::::::::::::::::::



    #::::::start event module url:::::
    #:::::::::::::::::::::::::::::::::


    url(r'^event/$', views.Event.as_view(), name='event'),
    url(r'^event/list/$', views.EventList.as_view(), name='event-list'),
    url(r'^event/list/(?P<pk>[0-9]+)/$', views.EventView.as_view(), name='event-view'),


    #:::::::end event module url::::::
    #:::::::::::::::::::::::::::::::::


    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::api::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    url(r'^attendance/api/$', views.AttendanceAPIPresent.as_view(), name='attendence-api'),

]
