from django.shortcuts import render

# Create your views here.

def test(request):
    return render(request,'base_event_origin.html')

def get_demo(request):
    return render(request,'get_demo.html')

def event1(request):
    return render(request,'input_demo1.html')

def event2(request):
    return render(request,'input_demo2.html')

def event3(request):
    return render(request,'input_demo3.html')

def event4(request):
    return render(request,'input_demo4(1).html')

def event5(request):
    return render(request,'input_demo5.html')

def event6(request):
    return render(request,'input_demo6.html')

def event7(request):
    return render(request,'input_demo7(1).html')

def event8(request):
    return render(request,'input_demo8.html')

def event9(request):
    return render(request,'input_demo9.html')

def news(request):
    return render(request,'input_demo1.html')

def event(request):
    return render(request, 'input_demo4(1).html')

def gkg(request):
    return render(request, 'input_demo7(1).html')