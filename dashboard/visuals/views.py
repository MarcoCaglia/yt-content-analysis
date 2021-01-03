import os
from pathlib import Path

from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = Path(os.getenv("DATA_PATH")).parent

# Create your views here.


def home(request):
    # Just return base html page
    return render(request, "visuals/base.html")


def overviews(request):
    # Load in all overview graphs
    for 
