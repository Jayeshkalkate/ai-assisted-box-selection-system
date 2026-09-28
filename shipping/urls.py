from django.urls import path
from . import views

urlpatterns = [
    path("recommend-box/", views.recommend_box_view, name="recommend-box"),
    path("orders/<str:reference>/box/", views.order_box_view, name="order-box"),
]
