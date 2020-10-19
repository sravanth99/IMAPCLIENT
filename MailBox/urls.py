from django.urls import path
from . import views
urlpatterns = [
    #path('',views.buffer,name='home'),
    #path('oth',views.other,name='other'),
    path('<str:foldername>/<str:uid>',views.pageview,name='ind-view'),
    path(r'<str:foldername>/page/<int:page_num>',views.other,name= 'pagenated'),
    path('',views.loginview,name='login'),
    path('...',views.logoutview,name='logout'),
]
