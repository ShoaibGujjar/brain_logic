from django.urls import path
from . import views

urlpatterns = [
    # login with jwt authentication.
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('ip/', views.get_client_ip),


    # all lower part consist on extar urls call for
    # registeruser
    # path('register/', views.registerUser, name="register"),
    # getuser
    # path('profile/', views.getUserProfile, name="customers-profile"),
    # update user profile
    # path('profile/update/', views.updateUserProfile, name="customers-profile-update"),
    # getallusers
    # path('getcustomers/', views.getUsers, name="customers"),
]
