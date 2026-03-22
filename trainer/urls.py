"""
Маршруты приложения trainer.
"""
from django.urls import path
import trainer.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('lattices/', views.lattice_table, name='lattice_table'),
    path('quiz/', views.quiz_setup, name='quiz_setup'),
    path('quiz/question/', views.quiz_question, name='quiz_question'),
    path('quiz/result/', views.quiz_result, name='quiz_result'),
]
