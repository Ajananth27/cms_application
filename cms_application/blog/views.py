from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from blog.serializer import *

class Login(APIView):
    def get(self, request):
        return render(request, "login.html")

@api_view(["GET", "POST"])
def user_resgister(request):
    if request.method == "POST":
        data = request.data
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        if not (username and email and password):
            return JsonResponse({"status": False, "message": "Please Check all the inputs."})
        user, created = User.objects.get_or_create(username=username, email=email)
        if created:
            user.set_password(password)
            user.save()
            messages.success(request, 'User register successful')
            return redirect("/")
        else:
            messages.error(request, "User already Exists.")
            return redirect("/register")
    else:
        return render(request, "register.html")

@csrf_exempt
def user_login(request):
    if request.POST:
        username = request.POST.get("username").strip()
        password = request.POST.get("password")
        if username is None or password is None:
            messages.error(request, "Please enter all inputs")
            return redirect("/")
        user = authenticate(request, username=username, password=password)
        if user:
            django_login(request, user)
            return redirect("/home")
        else:
            messages.error(request, "Invalid UserName or Password")
            return redirect("/")
    else:
        messages.error(request, "Invalid UserName or Password")
        return redirect("/")

def logout(request):
    from django.contrib import auth
    auth.logout(request)
    return redirect('/')

class BlobGet(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            if "id" in kwargs:
                blog = Blog.objects.filter(id=kwargs["id"])
                serialize_data = BlobListSerializer(blog, many=True).data
            else:
                blog_lists = Blog.objects.filter(is_deleted=False).order_by("-created_at")
                serialize_data = BlobListSerializer(blog_lists, many=True).data
            return render(request, "home.html", {"data": serialize_data})
        except Exception as e:
            return render(request, "home.html", {"data": {}})

class BlobCreate(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return render(request, "create_blog.html")

@api_view(["POST", "GET"])
@permission_classes((IsAuthenticated,))
def create_blogs(request, **kwargs):
    print("khjn")
    try:
        if request.method == "GET":
            if "id" in kwargs:
                blog = Blog.objects.get(id=kwargs["id"])
                ser_data = BlobSerializer(blog).data
                return render(request, "create_blog.html", {"data":ser_data})
            else:
                return render(request, "create_blog.html")
        else:
            data = request.POST
            blob_d = {
                "title": data["title"],
                "content": data["content"],
                "author": data["author"],
                "created_by_id": request.user.id
            }
            serializ_data = BlobSerializer(data=blob_d)
            if serializ_data.is_valid():
                serializ_data.save()
                messages.success(request, "Blog published successfully.")
                return redirect("/home")
            else:
                messages.error(request, "Please enter all the inputs")
                return redirect("home1")
    except Exception as e:
        messages.error(request, e)
        return redirect("home1")

@permission_classes((IsAuthenticated,))
def delete_blog(request, **kwargs):
    try:
        blog_id = kwargs["id"]
        blog = Blog.objects.get(id=blog_id)
        blog.is_deleted = True
        blog.save()
        messages.success(request, "Blog deleted successfully")
        return redirect("home")
    except Exception as e:
        messages.error(request, e)
        return redirect("home")
