from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list_create,name='category_list_create'),
    path('course/', views.course_list_create,name='course_list_create'),
    path('lesson/', views.lesson_list_create,name='lesson_list_create'),
    # path('material/', views.material_list_create,name='material_list_create'),
    # path('enrollment/', views.enrollment_list_create,name='enrollment_list_create'),
    # path('question-answer/', views.question_answer_list_create,name='question_answer_list_create'),
]