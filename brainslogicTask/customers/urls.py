from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('ip/',views.get_client_ip),

    # all lower part consist on extar urls call for 1)registeruser 2)update 3)getuser and 4)getallusers
    # path('register/', views.registerUser, name="register"),
    # path('profile/', views.getUserProfile, name="customers-profile"),
    # path('profile/update/', views.updateUserProfile, name="customers-profile-update"),
    # path('getcustomers/', views.getUsers, name="customers"),
]