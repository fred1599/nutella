from django.urls import path

from . import views

urlpatterns = [
    path('page/<int:page_number>/', views.product_view),
    path('save/<str:product>/', views.save_view),
    path('save/', views.save),
    path('delete/<str:product>/', views.delete),
    path('perso/', views.display, name='display'),
]
