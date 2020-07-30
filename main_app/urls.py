from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('new', views.new),
    path('create', views.create),
    path('delete_project/<int:proj_id>', views.delete_project),
    path('view/<int:proj_id>', views.detail),
    path('edit_project/<int:proj_id>', views.edit_project),
    path('remove_user/<int:proj_id>', views.remove_user),
    path('clockin/<int:proj_id>', views.clockin),
    path('clockout/<int:proj_id>', views.clockout),
    path('delete_time/<int:time_id>', views.delete_time),
    path('new_note/<int:proj_id>', views.new_note),
    path('profile', views.view_profile),
    path('create_file', views.create_post),
]