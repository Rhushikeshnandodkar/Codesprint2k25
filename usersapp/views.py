from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# Create your views here.
def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user)
            return redirect('/rooms/dashboard')  # Replace 'home' with your desired redirect URL name
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')