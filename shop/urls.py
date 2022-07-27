
from django.urls import path
from .import views

urlpatterns = [
    # path("",views.index,name="Shop"),
    path("",views.index,name="index"),
    path("index/",views.index,name="index"),
    path("about/",views.about,name="about"),

    path("contact/",views.contact,name="contactUs"),
    path("tracker/",views.tracker,name="tracker"),
    path("search/",views.search,name="search"),
    path("products/<int:myid>",views.productview,name="productView"),
    path("checkout/",views.checkout,name="Checkout"),
    path("handlerequest/",views.handlerequest,name="HandleRequest"),
    # path("cart/",views.cart,name="Cart"),
]
