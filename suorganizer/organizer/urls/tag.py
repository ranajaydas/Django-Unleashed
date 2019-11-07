from django.urls import path
from ..views import tag_list, tag_detail, TagCreate, TagUpdate, TagDelete


urlpatterns = [
    path('', tag_list, name='organizer_tag_list'),
    path('create/', TagCreate.as_view(), name='organizer_tag_create'),
    path('<slug>', tag_detail, name='organizer_tag_detail'),
    path('<slug>/update', TagUpdate.as_view(), name='organizer_tag_update'),
    path('<slug>/delete', TagDelete.as_view(), name='organizer_tag_delete'),
]
