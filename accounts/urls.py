from django.urls import path
from . import views

urlpatterns = [
	#path('home/<str:pk>/', views.home,name='home'),
	#path('home/<str:r_code>/', views.home,name='home'),

	path('home', views.home,name='home'),
	path('referrals/<str:ref_code>/', views.referrals, name='referrals'),
	path('referrals/', views.referrals, name='referrals'),
	path('', views.landing,name='landing'),
	path('simple_upload/', views.simple_upload,name='simple_upload'),
	path('gigs/', views.gigs,name='gigs'),
	path('login/', views.loginPage,name='login'),
	path('logout/', views.logoutUser,name='logout'),
	path('writers/<str:pk>/', views.writers,name='writers'),
	#path('writers/', views.writers,name='writers'),
	path('signup/', views.signup,name='signup'),
	path('withdraw/', views.withdraw,name='withdraw'),
	path('pay/', views.pay,name='pay'),
	path('forget/', views.forget,name='forget'),
	path('daraja/stk-push', views.stk_push_callback, name='mpesa_stk_push_callback'),
	path('plans/', views.MembershipView.as_view(), name='plans'),
	
]
