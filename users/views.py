from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Wrong email'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Delete the user's authentication token
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)
    

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "message": "User updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({
            "message": "User deleted successfully",
            "data": UserSerializer(instance).data
        }, status=status.HTTP_200_OK)
    

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            # Check if the old password matches
            if not self.object.check_password(old_password):
                return Response({"error": "The old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            # Set and save the new password
            self.object.set_password(new_password)
            self.object.save()

            return Response({"message": "Password changed successfully"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
