from django.urls import re_path
from .views import main_view, signup_view, my_recommendations_view, dashboard,\
    cryptocurrency, login_view, check_username, ProfileView, DepositPaymentMethodView,\
    DepositPaymentMethodDetailView, deposit_confirmation_view, WithdrawalRequestView

urlpatterns = [
    re_path('^$', main_view, name='main_view'),
    re_path('referrals/', my_recommendations_view, name='referrals'),
    re_path('signup/', signup_view, name='signup_view'),
    re_path('signin/', login_view, name='signin_view'),
    re_path('dashboard/', dashboard, name='dashboard'),
    re_path('crypto/', cryptocurrency, name='cryptocurrency'),
    re_path('profile/', ProfileView.as_view(), name='profile'),
    re_path('deposit-payment-method/', DepositPaymentMethodView.as_view(), name='deposit-payment-method'),
    re_path('(?P<pk>\d+)/', DepositPaymentMethodDetailView.as_view(), name='deposit-payment-method-detail'),
    re_path('dconf/', deposit_confirmation_view, name='deposit-confirmation'),
    re_path('wid/', WithdrawalRequestView.as_view(), name='wid'),
]

htmx_urlpatterns = [
    re_path('check_username/', check_username, name='check-username')
]

urlpatterns += htmx_urlpatterns