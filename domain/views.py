from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DomainDetails
from .serializers import DomainDetailsSerializer

class DomainDetailsListCreateView(generics.ListCreateAPIView):
    queryset = DomainDetails.objects.filter(is_active=True,is_deleted=False)
    serializer_class = DomainDetailsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "Domain detail created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DomainDetailsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DomainDetails.objects.all()
    serializer_class = DomainDetailsSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "message": "Domain detail updated successfully",
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
            "message": "Domain detail deleted successfully",
            "data": instance_data
        }, status=status.HTTP_204_NO_CONTENT)


