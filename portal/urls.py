from django.urls import path                                # ^_^ ENTERED MANUALLY ^_^
from . import views                                         # ^_^ ENTERED MANUALLY ^_^

urlpatterns = [                                             # ^_^ ENTERED MANUALLY ^_^
    path('', views.home, name='home'),                      # ^_^ ENTERED MANUALLY ^_^
    path('login',views.login,name='login'),                 # ^_^ ENTERED MANUALLY ^_^
    path('register',views.register,name='register'),        # ^_^ ENTERED MANUALLY ^_^
    path('portal',views.portal,name='portal') ,
    path('logout',views.logout,name='logout'),                                                        # ^_^ ENTERED MANUALLY ^_^
    path('vehicle_create',views.vehicle_create_view,name='vehicle_create'),
    path('rule_engine',views.rule_engine_view,name='rule_engine'),
    path('service_bikes',views.service_bikes,name='service_bikes'),
    path('check',views.check,name='check'),             #for odo meter update
    path('servicedue',views.servicedue,name='servicedue'),                #for service due check
    path('update', views.update, name='update'),                       #for update service details

]                                                           # ^_^ ENTERED MANUALLY ^_^
