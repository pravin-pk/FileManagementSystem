from django.db.models.fields import EmailField
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from SFMS import models
from django.db import connections

# Create your views here.
def index(response):
    return HttpResponse('<h1>Student File Management System</h1>')

def StudentLogin(request):
    return render (request, "StudentLogin.html")

def StudentReg(request):
    return render(request, "StudentReg.html")

def error_404(request,exception):
    return render(request, "404.html")

def doLogin(request):
    if(request.method!='POST'):
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        user = request.POST.get("your_username")
        password = request.POST.get("your_pass")
        p = models.Registration.objects.raw(f"SELECT * FROM Registration WHERE Username = '{user}' AND  Pass = md5('{password}');")

        if(p):
            return HttpResponse("<h2>Login Successful</h2>")
        else:
            messages.info(request,'Username or Password is incorrect!')
            return render(request,"StudentLogin.html")

def doReg(request):
    if(request.method!='POST'):
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        user = request.POST.get("username")
        usn = request.POST.get("usn")
        email =request.POST.get("email")
        college =request.POST.get("college")
        branch =request.POST.get("branch")
        passw = request.POST.get("pass")
        re_pass =request.POST.get("re_pass")

        if(passw==re_pass):
            cursor = connections['default'].cursor()
            cursor.execute(f"INSERT INTO Registration VALUES('{usn}','{user}','{email}',md5('{passw}'),'{branch}','{college}');")
            return HttpResponse("<h2>Registration Successful</h2>")
        else:
            return render(request,"StudentReg.html")

def trial(request): #trial purpose
    posts = models.Registration.objects.all()
    print(posts)
    print(posts.query)

    p=models.Registration.objects.raw('SELECT * FROM Registration')[0]
    print(p.username,p.email)
    
    return HttpResponse("hello")
