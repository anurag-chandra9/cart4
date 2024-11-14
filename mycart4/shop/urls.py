from django.urls import path
from.import views
urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("about/",views.about,name="Aboutus"),
    path("contact/",views.contact,name="contactus"),
    path("tracker/",views.tracker,name="trackingstatus"),
    path("search/",views.search,name="search"),
    path("products/<int:myid>", views.productview, name="Productview"),
    path("checkout/",views.checkout,name="checkout"),
    path("handlerequest/",views.handlerequest,name="Handlerequest"),
]