from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('new', views.new),
    path('create', views.create),
    path('delete/<int:proj_id>', views.delete),
    path('view/<int:proj_id>', views.detail),
    path('edit/<int:proj_id>', views.edit),
    path('remove/<int:proj_id>', views.remove),
    path('start_time/<int:proj_id>', views.start_time),
    path('end_time/<int:proj_id>', views.end_time),
]