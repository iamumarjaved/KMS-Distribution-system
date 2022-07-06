from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('',views.signin, name='signin'),
    path('signin/',views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('acc-type/', views.acc_type, name='acc-type'),
    re_path(r'^enter-sales/(?P<name>\w+)/$', views.enter_sales, name='enter-sales'),
    re_path(r'^enter-zonal/(?P<name>\w+)/$', views.enter_zonal, name='enter-zonal'),
    path('test/', views.test, name='test'),
    path('director-detail/', views.director_detail, name='director-detail'),
    re_path(r'^dashboard/enter-products.html/(?P<name>\w+)/$', views.enter_products, name='enter-products'),
    re_path(r'^dashboard/chose-form.html/(?P<name>\w+)/$', views.chose_form, name='chose-form'),
    re_path('dashboard/(?P<name>\w+)/$', views.dashboard, name='dashboard'),
    re_path(r'^dashboard/order/(?P<name>\w+)/$', views.order, name='order'),
    re_path(r'^dashboard/give-order.html/(?P<name>\w+)/$', views.give_order, name='give-order'),
    re_path(r'^dashboard/total_sales.html/(?P<name>\w+)/$', views.total_sales, name='total-sales'),
    re_path(r'^dashboard/total_sales/person_chart.html/(?P<name>\w+)/$', views.person_chart, name='person-chart'),
    # re_path(r'^dashboard/chose-form/give-order/cart.html/(?P<name>\w+)/$', views.cart, name='cart'),
]
