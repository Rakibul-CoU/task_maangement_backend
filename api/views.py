from django.shortcuts import render
from rest_framework.views import APIView

from api.models import CustomUser, Task
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number', None)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if phone_number and CustomUser.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create(
            email=email,
            username=username,
            password=make_password(password),
            phone_number=phone_number,
        )

        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Login successful.",
            "access": access_token,
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


class TaskListView(APIView):
    def get(self, request):
        tasklist = Task.objects.all()
        context = {}
        task_list = []
        for i in tasklist:
            task_dict = {}
            task_dict['id'] = i.pk
            task_dict['name'] = i.name
            task_dict['description'] = i.description
            task_list.append(task_dict)
        context['task_list'] = task_list
        return Response(context, status = status.HTTP_200_OK)
    

class TaskEditView(APIView):
    def put(self, request, task_id):
        # Fetch the task object or return a 404 if not found
        task = get_object_or_404(Task, id=task_id)
        
        # Get the updated data from the request
        name = request.data.get("name")
        description = request.data.get("description")
        
        # Validate and update the task
        if name:
            task.name = name
        if description:
            task.description = description
            
        # Save the updated task object
        task.save()
        
        # Return a success response
        return Response({
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "message": "Task updated successfully."
        }, status=status.HTTP_200_OK)
    


class TaskAddView(APIView):
    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')

        task = Task()
        task.name = name
        task.description = description
        task.save()

        return Response({
            "id" : task.id,
            "name" : task.name,
            "description" : task.description,
            "message" : "Task Created Successfully!"
        })
    

class HomeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        context = {}

        return Response(context, status=status.HTTP_200_OK)

