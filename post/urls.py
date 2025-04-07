from django.urls import path
from .views import list_view, write_veiw, detail_veiw

app_name = 'post'

urlpatterns = [
    path('list/', list_view, name="list"),
    path('write/', write_veiw, name="write"),
    path('detail/<int:post_id>/', detail_veiw, name="detail"),
]