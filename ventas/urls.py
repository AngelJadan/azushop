from django.contrib import admin
from django.urls import path
from ventas import views

urlpatterns = [
    path("list-all-products/", views.ListAllProduct.as_view(), name="list-all-products"),
    path("api-facebook-consumer/", views.api_facebook_consumer, name="api_facebook_consumer"),
    path("view_list_images/", views.view_list_images, name="view_list_images"),
    path("publish_product/<int:id_product>/", views.publish_product, name="publish_product"),
    path("image/<int:id_catalog>/", views.image, name="image"),
    path("view_products_recomeders/<int:id_product>/", views.View_products_recomeders.as_view(), name="view_products_recomeders"),
    path("car-api/", views.CarAPI.as_view(), name="car-api"),
    path("car-api/<int:pk>/", views.CarAPI.as_view(), name="car-api-id"),
    path("list-car/<int:client>/", views.ListCar.as_view(), name="list_car"),
    path("bilding/", views.BildingAPI.as_view(), name="bilding"),
    path("list-bildings/<int:client>/", views.ListBildingsClient.as_view(), name="list-bildings-client"),
    path("view_bilding/<int:id_bilding>/", views.view_bilding, name="view_bilding"),
]
