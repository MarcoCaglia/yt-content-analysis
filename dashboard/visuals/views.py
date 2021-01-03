from django.shortcuts import render

# Create your views here.


def welcome(request):
    # Just return base html page
    return render(request, "visuals/base.html")
