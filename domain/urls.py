from django.urls import path
from .views import DomainDetailsListCreateView, DomainDetailsRetrieveUpdateDestroyView

urlpatterns = [
    path('domain', DomainDetailsListCreateView.as_view(), name='domain-details-list-create'),
    path('domain/<int:pk>', DomainDetailsRetrieveUpdateDestroyView.as_view(), name='domain-details-retrieve-update-destroy'),
]
