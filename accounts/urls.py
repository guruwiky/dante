from django.urls import path
from . import views

urlpatterns = [
	path('', views.home,name='home'),
	path('landing/', views.landing,name='landing'),
	path('simple_upload/', views.simple_upload,name='simple_upload'),
	path('gigs/', views.gigs,name='gigs'),
	path('login/', views.loginPage,name='login'),
	path('logout/', views.logoutUser,name='logout'),
	path('writers/<str:pk>/', views.writers,name='writers'),
	path('signup/', views.signup,name='signup'),
	path('forget/', views.forget,name='forget'),
]
	