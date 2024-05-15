from django.urls import path
from . import views
from admin_panel.views import report_project, report_comment

urlpatterns = [
    path('<int:project_id>/', views.detail, name='detail'),
    path('<int:project_id>/vote/', views.vote, name='vote'),
    path('<int:project_id>/add_comment', views.add_comment, name='add_comment'),
    path('<int:project_id>/report_project', report_project, name='report_project'),
    path('<int:comment_id>/report_comment', report_comment, name='report_comment'),
]