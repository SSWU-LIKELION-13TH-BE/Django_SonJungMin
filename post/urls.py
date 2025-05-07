from django.urls import path
from .views import list_view, write_view, detail_view, comment_view, post_likes_view, comment_likes_view, search_view, post_update_view, post_delete_view

app_name = 'post'

urlpatterns = [
    path('list/', list_view, name="list"),
    path('write/', write_view, name="write"),
    path('detail/<int:post_id>/', detail_view, name="detail"),
    path('detail/<int:post_id>/comment/', comment_view, name="comment"),
    path('detail/<int:post_id>/likes/', post_likes_view, name="post_likes"),
    path('detail/likes/<int:comment_id>/', comment_likes_view, name="comment_likes"),
    path('search/', search_view, name='search'),
    path('post_update/<int:post_id>/', post_update_view, name="post_update"),
    path('post_delete/<int:post_id>/', post_delete_view, name="post_delete"),
]