from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-list-product/', ListProductAPIView.as_view(), name='get_list_all_product'),
    path('api-search-products/', SearchProductAPIView.as_view() , name='search_products'),
    path('api-receiving-product/<int:pk>', ReceivingProductAPIView.as_view(), name='receiving_an_product'),
    path('api-create-order/', CreateOrderAPIView.as_view(), name='create_order'),
    path('api-change-status-order/<int:pk>', UpdateStatusOrderAPIView.as_view(), name='update_status_order'),
    path('api-acceptance-of-payment/<int:pk>', AcceptancePaymentAPIView.as_view(), name='acceptance_of_payment'),
    path('api-date-search-orders/', SearchOrderAPIView.as_view(), name='search_orders_by_date'),
]