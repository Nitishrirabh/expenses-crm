from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Expenses
from .serializers import ExpensesSerializer

class ExpensesListCreateView(generics.ListCreateAPIView):
    queryset = Expenses.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            # If the request data is a list, handle multiple creation
            serializers = [self.get_serializer(data=expense) for expense in request.data]
            if all(serializer.is_valid() for serializer in serializers):
                self.perform_bulk_create(serializers)
                return Response({
                    "message": "Expenses created successfully",
                    "data": [serializer.data for serializer in serializers]
                }, status=status.HTTP_201_CREATED)
            errors = [serializer.errors for serializer in serializers if not serializer.is_valid()]
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle single creation
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({
                    "message": "Expense created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def perform_bulk_create(self, serializers):
        for serializer in serializers:
            self.perform_create(serializer)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class ExpensesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "message": "Expense updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Perform soft delete
        instance.is_active = False
        instance.is_deleted = True
        instance.save()
        instance_data = self.get_serializer(instance).data
        return Response({
            "message": "Expense deleted successfully",
            "data": instance_data
        }, status=status.HTTP_204_NO_CONTENT)

