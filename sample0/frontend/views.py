from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render (request, 'index.html')

def about(request):
    return render (request, 'about.html')

def industries(request):
    return render (request, 'industries.html')

def contact(request):
    return render (request, 'contact.html')
    