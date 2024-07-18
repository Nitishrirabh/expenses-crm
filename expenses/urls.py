from django.urls import path
from .views import ExpensesListCreateView, ExpensesRetrieveUpdateDestroyView

urlpatterns = [
    path('expenses', ExpensesListCreateView.as_view(), name='expenses-list-create'),
    path('expenses/<int:pk>', ExpensesRetrieveUpdateDestroyView.as_view(), name='expenses-retrieve-update-destroy'),
]
