from django.urls import path, include, re_path
from . import views
# from djoser.views import UserView, UserCreateViewfrom, TokenCreateView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
#     path('/', include('djoser.urls')),
#     path('users/', UserCreateViewfrom.as_view(), name='user_create'),
#     path('users/me/', UserView.as_view(), name='user_view'),
#     path('token/login/', TokenCreateView.as_view(), name='token_obtain_pair'),

    re_path(r"^", include("djoser.urls.base")),
    re_path(r"^", include("djoser.urls.authtoken")),
    re_path(r"^", include("djoser.urls.jwt")),

    path('menu-items/category', views.CategoryView.as_view(), name='categorylist'),
    path('menu-items/category/<int:pk>',
         views.SingleCategoryView.as_view(), name='category'),
    path('menu-items', views.MenuItemView.as_view(), name='menuitemlist'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menuitem'),
    path('cart/menu-items', views.CartView.as_view(), name='cartlist'),
    # path('cart/<int:pk>', views.SingleCartView.as_view(), name='cart'),
    path('orders', views.OrderView.as_view(), name='orderlist'),
    path('orders/<int:pk>', views.SingleOrderView.as_view(), name='order'),

    path('groups/managers/users', views.ManagersListView.as_view()),
    path('groups/managers/users/<int:pk>', views.ManagersRemoveView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewListView.as_view()),
    path('groups/delivery-crew/users/<int:pk>',
         views.DeliveryCrewRemoveView.as_view()),
]
