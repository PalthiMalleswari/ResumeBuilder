from . import views
from django.urls import path
from .views import ResumeListView, ResumeDetailView, UseTemplateView
from .auth_views import LoginView, LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('resumes/', ResumeListView.as_view(), name='resume-list'),
    path('resume/<int:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
    path('resume/<int:pk>/use/', UseTemplateView.as_view(), name='use-template'),
    path('generate-resume/', views.generate_resume, name='generate-resume'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
