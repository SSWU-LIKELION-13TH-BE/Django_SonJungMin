from django.urls import path
from .views import list_view, write_veiw, detail_veiw, comment_view, post_likes_view, comment_likes_view, search_veiw, list_sort_view

app_name = 'post'

urlpatterns = [
    path('list/', list_view, name="list"),
    path('write/', write_veiw, name="write"),
    path('detail/<int:post_id>/', detail_veiw, name="detail"),
    path('detail/<int:post_id>/comment/', comment_view, name="comment"),
    path('detail/<int:post_id>/likes/', post_likes_view, name="post_likes"),
    path('detail/likes/<int:comment_id>/', comment_likes_view, name="comment_likes"),
    path('search/', search_veiw, name='search'),
    path('list_sort/', list_sort_view, name="list_sort"),
]