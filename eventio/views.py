from django.shortcuts import render

def index(request):
	return render(request, 'index.html')
def contact_us(request):
    return render(request,'contact_us.html')
def about(request):
    return render(request,'about.html')
def login(request):
	return render(request, 'login.html')
def register(request):
	return render(request, 'register.html')