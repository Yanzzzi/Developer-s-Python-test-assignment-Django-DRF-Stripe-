from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('item/<int:item_id>/', ShowItem.as_view(), name='item'),
    path('buy/<int:pr_k>/', ItemBuyAPIView.as_view(), name='buy'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
]