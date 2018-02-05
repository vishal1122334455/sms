from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),

    #::::start member operation module url::::
    #:::::::::::::::::::::::::::::::::::::::::

    url(r'^office-registration/$', views.Registration.as_view(), name='office-registration'),

    #member operations
    url(r'^member/search/$', views.MemberSearch.as_view(), name='member-search'),

    #list of member
    url(r'^member/list/$', views.MemberList.as_view(), name='member-list'),
    url(r'^member/list/(?P<type>[a-zA-Z]+)/$', views.MemberListDetail.as_view(), name='member-list-detail'),

    #list of class in student
    url(r'^member/list/student/class/$', views.StudentClass.as_view(), name='student-class'),
    url(r'^member/list/student/class/(?P<classes>[a-zA-Z0-9]+)/$', views.StudenListInClass.as_view(), name='student-list-in-class'),

    #list of section in class
    url(r'^member/list/student/class/(?P<classes>[a-zA-Z0-9]+)/section/$', views.ClassWiseSection.as_view(), name='section'),
    url(r'^member/list/student/class/(?P<classes>[a-zA-Z0-9]+)/section/(?P<section>[a-zA-Z0-9-_]+)/$', views.SectionWiseStudent.as_view(), name='section-wise-student'),

    url(r'^member/detail/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view(), name='member-detail'),
    url(r'^member/edit/(?P<pk>[0-9]+)/$', views.MemberEdit.as_view(), name='member-edit'),
    url(r'^member/delete/(?P<pk>[0-9]+)/$', views.MemberDelete.as_view(), name='member-delete'),

    #:::::::::::::::::::::::::::::::::::::::
    #::::end member operation module url::::


    #::::start schedule module url::::
    #:::::::::::::::::::::::::::::::::


    url(r'^schedule/$', views.Schedule.as_view(), name='schedule'),
    url(r'^schedule/class-list/$', views.ClassList.as_view(), name='class-list'),
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/$', views.SectionList.as_view(), name='section-list'),

    #create routine
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/(?P<section>[a-zA-Z0-9-_]+)/routine/create/$', views.RoutineCreate.as_view(), name='routine-create'),
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/(?P<section>[a-zA-Z0-9-_]+)/routine/view/$', views.RoutineView.as_view(), name='routine-view'),
    url(r'^schedule/routine/edit/(?P<pk>[0-9]+)/$', views.RoutineEdit.as_view(), name='routine-edit'),
    url(r'^schedule/routine/delete/(?P<pk>[0-9]+)/$', views.RoutineDelete.as_view(), name='routine-delete'),

    #create exam routine
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/exam-routine/create/$', views.ExamRoutineCreate.as_view(), name='exam-routine-create'),
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/exam-routine/view/$', views.ExamRoutineView.as_view(), name='exam-routine-view'),
    url(r'^schedule/class-list/exam-routine/edit/(?P<pk>[0-9]+)/$', views.ExamRoutineEdit.as_view(), name='exam-routine-edit'),
    url(r'^schedule/exam-routine/delete/(?P<pk>[0-9]+)/$', views.ExamRoutineDelete.as_view(), name='exam-routine-delete'),


    #::::end schedule module url::::
    #:::::::::::::::::::::::::::::::::



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


    #:::::start gallary module url::::
    #:::::::::::::::::::::::::::::::::

    url(r'^gallary/$', views.Gallary.as_view(), name='gallary'),
    url(r'^gallary/image/$', views.GallaryImage.as_view(), name='gallary-image'),
    url(r'^gallary/image/create/$', views.GallaryImageCreate.as_view(), name='gallary-image-create'),
    url(r'^gallary/image/view/$', views.GallaryImageView.as_view(), name='gallary-image-view'),
    url(r'^gallary/image/delete/(?P<pk>[0-9]+)/$', views.GallaryImageDelete.as_view(), name='gallary-image-delete'),


    url(r'^gallary/video/$', views.GallaryVideo.as_view(), name='gallary-video'),
    url(r'^gallary/video/create/$', views.GallaryVideoCreate.as_view(), name='gallary-video-create'),
    url(r'^gallary/video/view/$', views.GallaryVideoView.as_view(), name='gallary-video-view'),
    url(r'^gallary/video/delete/(?P<pk>[0-9]+)/$', views.GallaryVideoDelete.as_view(), name='gallary-video-delete'),

    #::::::end gallary module url::::::
    #:::::::::::::::::::::::::::::::::


    #::::start classroom module url:::
    #:::::::::::::::::::::::::::::::::

    url(r'^classroom/$', views.Classroom.as_view(), name='classroom'),
    url(r'^classroom/class-list/$', views.ClassroomClasslist.as_view(), name='classroom-classlist'),
    url(r'^classroom/(?P<classes>[a-zA-Z0-9]+)/section-list/$', views.ClassroomSectionlist.as_view(), name='classroom-sectionlist'),
    url(r'^classroom/(?P<classes>[a-zA-Z0-9]+)/(?P<section>[a-zA-Z0-9]+)/create/$', views.ClassroomCreate.as_view(), name='classroom-create'),
    url(r'^classroom/(?P<classes>[a-zA-Z0-9]+)/(?P<section>[a-zA-Z0-9]+)/view/$', views.ClassroomView.as_view(), name='classroom-view'),
    url(r'^classroom/(?P<pk>[0-9]+)/edit/$', views.ClassroomEdit.as_view(), name='classroom-edit'),
    url(r'^classroom/(?P<pk>[0-9]+)/delete/$', views.ClassroomDelete.as_view(), name='classroom-delete'),

    #:::::end classroom module url::::
    #:::::::::::::::::::::::::::::::::


    #::::::start event module url:::::
    #:::::::::::::::::::::::::::::::::


    url(r'^event/$', views.Event.as_view(), name='event'),
    url(r'^event/create/$', views.EventCreate.as_view(), name='event-create'),
    url(r'^event/list/$', views.EventList.as_view(), name='event-list'),
    url(r'^event/list/(?P<pk>[0-9]+)/$', views.EventView.as_view(), name='event-view'),
    url(r'^event/edit/(?P<pk>[0-9]+)/$', views.EventEdit.as_view(), name='event-edit'),
    url(r'^event/delete/(?P<pk>[0-9]+)/$', views.EventDelete.as_view(), name='event-delete'),


    #:::::::end event module url::::::
    #:::::::::::::::::::::::::::::::::


    #:::::start payment module url::::
    #:::::::::::::::::::::::::::::::::

    url(r'^payment/$', views.Payment.as_view(), name='payment'),

    #::::::end payment module url:::::
    #:::::::::::::::::::::::::::::::::



    #:::::start expense module url::::
    #:::::::::::::::::::::::::::::::::

    url(r'^expense/$', views.Expense.as_view(), name='expense'),
    url(r'^expense/catagory/$', views.ExpenseCatagory.as_view(), name='expense-catagory'),
    url(r'^expense/catagory/create/$', views.ExpenseCatagoryCreate.as_view(), name='expense-catagory-create'),
    url(r'^expense/catagory/view/$', views.ExpenseCatagoryView.as_view(), name='expense-catagory-view'),
    url(r'^expense/catagory/edit/(?P<pk>[0-9]+)/$', views.ExpenseCatagoryEdit.as_view(), name='expense-catagory-edit'),
    url(r'^expense/catagory/delete/(?P<pk>[0-9]+)/$', views.ExpenseCatagoryDelete.as_view(), name='expense-catagory-delete'),


    url(r'^expense/entry/$', views.ExpenseEntry.as_view(), name='expense-entry'),
    url(r'^expense/entry/create/$', views.ExpenseCreate.as_view(), name='expense-create'),
    url(r'^expense/entry/list/$', views.ExpenseList.as_view(), name='expense-list'),
    url(r'^expense/entry/list/(?P<catagory>[a-zA-Z0-9-_]+)/$', views.ExpenseListDetail.as_view(), name='expense-list-detail'),
    url(r'^expense/entry/detail/(?P<pk>[0-9]+)/$', views.ExpenseDetail.as_view(), name='expense-detail'),
    url(r'^expense/entry/edit/(?P<pk>[0-9]+)/$', views.ExpenseEdit.as_view(), name='expense-edit'),
    url(r'^expense/entry/delete/(?P<pk>[0-9]+)/$', views.ExpenseDelete.as_view(), name='expense-delete'),

    #::::::end expense module url:::::
    #:::::::::::::::::::::::::::::::::


    #:::::::start bus module url::::::
    #:::::::::::::::::::::::::::::::::

    url(r'^bus/$', views.Bus.as_view(), name='bus'),
    url(r'^bus/create/$', views.BusCreate.as_view(), name='bus-create'),
    url(r'^bus/view/$', views.BusView.as_view(), name='bus-view'),
    url(r'^bus/edit/(?P<pk>[0-9]+)/$', views.BusEdit.as_view(), name='bus-edit'),
    url(r'^bus/delete/(?P<pk>[0-9]+)/$', views.BusDelete.as_view(), name='bus-delete'),

    #::::::::end bus module url:::::::
    #:::::::::::::::::::::::::::::::::


    #:::::::start cass module url:::::
    #:::::::::::::::::::::::::::::::::


    url(r'^class/$', views.ClassHome.as_view(), name='class'),
    url(r'^class/create/$', views.ClassCreate.as_view(), name='class-create'),
    url(r'^class/list/$', views.ClassListView.as_view(), name='class-list-view'),
    url(r'^class/edit/(?P<pk>[0-9]+)/$', views.ClassListEdit.as_view(), name='class-list-edit'),
    url(r'^class/delete/(?P<pk>[0-9]+)/$', views.ClassListDelete.as_view(), name='class-list-delete'),


    #:::::::end class module url::::::
    #:::::::::::::::::::::::::::::::::
]
