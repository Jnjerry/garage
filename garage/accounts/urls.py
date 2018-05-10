from django.conf.urls import url,include
from django.views.generic import TemplateView
from .views import customer,mechanic,accounts


urlpatterns = [

    url('accounts/signup/mechanic/', mechanic.MechanicSignUpView.as_view(), name='mechanic_signup'),
    url('accounts/signup/customer/', customer.CustomerSignUpView.as_view(), name='customer_signup'),
    url('accounts/signup/', accounts.SignUpView.as_view(), name='signup'),


    # url('pdf', accounts.GeneratePdf.as_view(), name='pdf'),
    url('^$', accounts.home, name='home'),




    url('customer/', include(([



    url('vehicle_delete/(?P<pk>[0-9]+)',customer.VehicleDeleteView.as_view(),name='vehicle_delete'),
    url('dashboard', customer.custdashboard, name='custdashboard'),
    url('vehicle/list', customer.VehicleListView.as_view(), name='vehicle_list'),
    url('vehicleupdate/(?P<pk>[0-9]+)',customer.VehicleUpdateView.as_view(),name='vehicle_change'),
    url('vehicle/add',customer.VehicleCreateView.as_view(),name='vehicle_add'),


    url('regular_service/add',customer.RegularServiceCreateView.as_view(),name='regular_service_add'),
    url('regular_service/list',customer.RegularServiceListView.as_view(),name='regular_service_list'),
    url('regular_service/update/(?P<pk>[0-9]+)',customer.RegularServiceUpdateView.as_view(),name='regular_service_change'),
    url('regular_service/delete/(?P<pk>[0-9]+)',customer.RegularServiceDeleteView.as_view(),name='regular_service_delete'),

    #mechanic and reviews
    # url('add_review',customer.ReviewCreateView.as_view(),name='add_review').
    # url(r'^review/user/(?P<username>\w+)/$', customer.user_review_list, name='user_review_list'),
    url(r'^recommendation/$', customer.user_recommendation_list, name='user_recommendation_list'),
    url(r'^mechanic_review/add/(?P<mechprofile_id>[0-9]+)/$', customer.add_review, name='add_review'),

    # url('list',customer.MechListView.as_view(),name='mech_list'),
    #vehicle repair
    url(r'^mech_list$', customer.mech_list, name='mech_list'),
    url('vehiclerepair/add',customer.VehicleRepairCreateView.as_view(),name='repair_add'),
    url('vehiclerepair/list',customer.VehicleRepairListView.as_view(),name='repair_list'),

    #painting and dents
    url('paint_dent/add',customer.PaintCreateView.as_view(),name='paint_add'),
    url('paint_dent/list',customer.PaintListView.as_view(),name='paint_list'),



], 'accounts'), namespace='customer')),


    url('ratings/', include(([
    # url('add', accounts.RateCreateView.as_view(),name='rate_add'),
    # url('list',accounts.RateListView.as_view(),name='rate_list'),

], 'accounts'), namespace='accounts')),






    url('mechanic/', include(([
    url('profileupdate/(?P<pk>[0-9]+)',mechanic.MechanicUpdateView.as_view(),name='profile_change'),
    url('profiledelete/(?P<pk>[0-9]+)',mechanic.MechanicDeleteView.as_view(),name='profile_delete'),
    #url(r'^profiledetail/(?P<pk>[0-9]+)/$', mechanic.MechanicDetailView.as_view(), name='profile_detail'),
    url('dashboard', mechanic.mechdashboard, name='mechdashboard'),
    url('list',mechanic.MechListView.as_view(),name='mech_list'),
    url(r'^profiledetail/(?P<mechprofile_id>[0-9]+)/$', mechanic.profile_detail, name='profile_detail'),
     # url('Profile/Add',mechanic.ProfileCreateView.as_view(),name='profile_add'),

    url(r'^mechanic_review/add/(?P<mechprofile_id>[0-9]+)/$', mechanic.add_review, name='add_review'),


      ], 'accounts'), namespace='mechanic')),




]
