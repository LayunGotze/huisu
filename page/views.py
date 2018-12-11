from django.shortcuts import render

# Create your views here.

def test(request):
    return render(request,'demo.html')

def get_demo(request):
    return render(request,'get_demo.html')