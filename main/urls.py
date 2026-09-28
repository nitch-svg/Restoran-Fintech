from django.urls import path
from .views import index, menu, branch, about, xodimlar, savat, contact, add_savat, remove_savat, clear_savat, order

urlpatterns = [
    path('', index, name = 'home'),
    path('menu/', menu, name = 'menu'),
    path('filiallar/', branch, name = 'branch'),
    path('about/', about, name = 'about_us'),
    path('xodimlar/', xodimlar, name = 'xodimlar'),
    path('savat/', savat, name='savat'),
    path('aloqa/', contact, name='aloqa'),
    path('add/savat/<int:ovqat_id>/', add_savat, name = 'add_savat'),
    path('remove/savat/<int:savat_id>/', remove_savat, name='remove_savat'),
    path('remove/savat/<int:savat_id>/<int:one_delete>', remove_savat, name='delete_one_savat'),
    path('clear/savat/', clear_savat, name='clear_savat'),
    path("order/", order, name="order")
]  