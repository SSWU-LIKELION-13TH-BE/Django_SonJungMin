from django.urls import path
from .views import list_view, write_veiw, detail_veiw, comment_view

app_name = 'post'

urlpatterns = [
    path('list/', list_view, name="list"),
    path('write/', write_veiw, name="write"),
    path('detail/<int:post_id>/', detail_veiw, name="detail"),
    path('detail/<int:post_id>/comment/', comment_view, name="comment"),
]