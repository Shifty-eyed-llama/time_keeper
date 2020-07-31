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
    path('profile/<int:worker_id>', views.view_profile),
    path('create_file', views.create_post),
    path('new_comment/<int:proj_id>', views.new_comment),
    path('join_project/<int:proj_id>', views.join_project),
    path('join_project_stay/view/<int:proj_id>', views.join_project_stay),
    path('leave_project/<int:proj_id>', views.leave_project),
    path('set_timezone', views.set_timezone),
]