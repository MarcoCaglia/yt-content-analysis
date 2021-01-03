import os
from pathlib import Path

from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = Path(__file__).parent.parent.joinpath(os.getenv("DATA_PATH"))

# Create your views here.


def home(request):
    # Just return base html page
    return render(request, "visuals/base.html")


def overviews(request):
    # Navigate to folder where overview graphs are stored
    overviews_folder = DATA_PATH.joinpath("overviews")

    # Generate graphs paths
    graphs_paths = overviews_folder.iterdir()

    # Load all graphs
    graph_htmls = []
    for path in graphs_paths:
        with path.open("r") as f:
            graph_htmls.append(f.read())

    return render(
        request,
        "visuals/graphs.html",
        {"graphs": graph_htmls, "title": {"Overview Graphs"}}
        )


def ot_graphs(request):
    # Navigate to folder where OT graphs are stored
    overviews_folder = DATA_PATH.joinpath("ot_graphs")

    # Generate graphs paths
    graphs_paths = overviews_folder.iterdir()

    # Load all graphs
    graph_htmls = []
    for path in graphs_paths:
        with path.open("r") as f:
            graph_htmls.append(f.read())

    return render(
        request,
        "visuals/graphs.html",
        {"graphs": graph_htmls, "title": "Overtime Graphs"}
        )
