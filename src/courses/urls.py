from django.urls import path

from . import views
from . import adminviews

urlpatterns = [
    path('', views.ListCourseView.as_view(), name="course-list"),
    path('<int:id>/', views.DetailCourseView.as_view(), name="course-detail"),
    path('lesson/<int:id>/', views.DetailLessonView.as_view(), name="lesson-detail"),
    path('check_work/', views.StudentWorkView.as_view(), name="check-work"),
    path('help_mentor/', views.HelpUserView.as_view(), name="help-mentor"),
    path('admin/', adminviews.AdminCourseView.as_view({"get": "list", "post": "create"}), name="admin-courses"),
    path('admin/repo/', adminviews.RepositoryView.as_view())
]