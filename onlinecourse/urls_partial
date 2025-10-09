from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='index'),                  # Home page - list courses
    path('registration/', views.registration_request, name='registration'),  # Register
    path('login/', views.login_request, name='login'),                        # Login
    path('logout/', views.logout_request, name='logout'),                     # Logout
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),  # Course detail
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),               # Enroll
    
    # Add route for submit view
    path('<int:course_id>/submit/', views.),

    # Add route for show_exam_result view
    path('course/<int:course_id>/submission/<int:submission_id>/result/', 
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
